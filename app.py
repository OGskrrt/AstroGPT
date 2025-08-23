from fastapi import FastAPI, Form, HTTPException
import requests
import os
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware


# Basic log level infos
import logging 
logging.basicConfig(level=logging.INFO)

# get root directory as where this .py is
ROOT_DIR = Path(__file__).resolve().parent
#print(ROOT_DIR)

STORE_DIR = ROOT_DIR / "faiss_store"
FAISS_PATH = STORE_DIR / "index_hnsw_ip.faiss"   
META_PATH  = STORE_DIR / "meta.parquet" 

HTML_DIR = ROOT_DIR / "templates" / "chat.html"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

st_model = SentenceTransformer(MODEL_NAME)
faiss_index = faiss.read_index(os.path.join(FAISS_PATH))
meta_df = pd.read_parquet(os.path.join(META_PATH))

logging.info(f"Model, FAISS and metadata loaded.")

OLLAMA_ENDPOINT = "http://localhost:11434"  
OLLAMA_MODEL = "llama3.1:8b"             

app = FastAPI(title="Space Cadet")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000", "*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def prepare_augmented_query(contexts: str, user_input: str, persona: str, topic: str, subtopic: str) -> str:

    augmented_query = f"""
        You are AstroGPT, an expert AI assistant specialized in space knowledge.
        The main topic is: {topic}.
        The subtopic is: {subtopic}.
        The user's question is: "{user_input}".         
        The person asking the question has the following characteristics: {persona}.

        You must answer ONLY based on the provided sources below. 
        Do not invent information outside these sources. 
        Adapt your answer to the persona's characteristics when possible.

        Sources:
        {contexts}

        Answer in English.
    """
    return augmented_query.strip()

def augment_query(user_input: str):
    #print(user_input)

    q_emb = st_model.encode([user_input], normalize_embeddings=True, convert_to_numpy=True).astype("float32")

    _, q_index = faiss_index.search(q_emb, 10)
    
    retrieved_texts = []
    for i in q_index[0]:
        if i == -1:
            continue
        retrieved_texts.append(meta_df.iloc[i]["text"])
    contexts = "\n\n".join(retrieved_texts)

    persona = meta_df.iloc[q_index[0][0]]["persona"]
    topic = meta_df.iloc[q_index[0][0]]["topic"]
    subtopic = meta_df.iloc[q_index[0][0]]["subtopic"]
        
    augmented_query = prepare_augmented_query(contexts, user_input, persona, topic, subtopic)

    return augmented_query

def call_ollama_with_prompt(prompt: str) -> str:
    url = f"{OLLAMA_ENDPOINT.rstrip('/')}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        r = requests.post(url, data=json.dumps(payload), timeout=120)
        r.raise_for_status()
        data = r.json()
        return (data.get("response") or "").strip() or "No response."
    
    except Exception as e:
        logging.warning(f"Ollama call failed: {e}")
        return "Could not reach the local LLM (Ollama). Is it running?"


@app.get("/", response_class=FileResponse)
def home_page():
    return FileResponse(HTML_DIR)

@app.post("/chat")
def chat_form(message: str = Form(...)):
    user_text = message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Empty message")
    
    augmented_query = augment_query(user_text)
    reply = call_ollama_with_prompt(augmented_query)
    
    return JSONResponse(reply)

from fastapi import Response
@app.get("/health")
def health():
    return Response(status_code=204)

@app.head("/")
def home_head():
    return Response(status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)


