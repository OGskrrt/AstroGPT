# AstroGPT 🚀

AstroGPT is a **learning-oriented project** built with **FastAPI**, **FAISS**, **SentenceTransformers**, and **Ollama**.  
The main goal is to practice the fundamentals of **Retrieval-Augmented Generation (RAG)**, experiment with FAISS for vector search, and integrate a local LLM through Ollama.

---

## 🛰 Technologies Used
- **FastAPI** → Backend REST service  
- **FAISS** → Vector search engine  
- **SentenceTransformers** → Embedding generation for queries and documents  
- **Ollama (LLaMA 3.1:8B)** → Language model  
- **HTML + Vanilla JS** → Frontend interface  
- **pandas / numpy** → Data processing  

---

## ⚙️ System Architecture
1. **Frontend (chat.html)** → Collects user messages, sends them to the backend, and renders responses.  
2. **Backend (FastAPI)**  
   - Generates embeddings for user queries.  
   - Retrieves the most relevant chunks using FAISS.  
   - Builds an augmented prompt and sends it to Ollama.  
   - Returns the model’s response to the frontend.  
3. **Ollama** → Generates the final answer using the retrieved context.  

---

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Start Ollama and pull the model:
    ```bash
    ollama run llama3.1:8b

3. Run the FastAPI app:
    ```bash
    uvicorn app:app --reload --port 8000

4. Open in your browser:
    ```bash
    http://localhost:8000
    


