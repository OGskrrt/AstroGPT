# AstroGPT 🚀

AstroGPT is a **learning-oriented project** built with **FastAPI**, **FAISS**, **SentenceTransformers**, and **Ollama**.  
The main goal is to practice the fundamentals of **Retrieval-Augmented Generation (RAG)**, experiment with FAISS for vector search, and integrate a local LLM through Ollama.
Data source : https://www.kaggle.com/datasets/patrickfleith/astrochat

<img width="1275" height="1271" alt="Screenshot 2025-08-24 005133" src="https://github.com/user-attachments/assets/a7bf0612-51b2-4847-a2f6-ea3cb34aaa67" />

<img width="1271" height="1264" alt="Screenshot 2025-08-24 005151" src="https://github.com/user-attachments/assets/235755bf-69c6-42e5-a631-8222476291b7" />

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
    


