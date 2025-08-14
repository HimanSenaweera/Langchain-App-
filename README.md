# 📚 Multi‑PDF Chatbot with LangChain & Streamlit

## 📌 Overview
This project is an interactive **PDF Q&A chatbot** built with **LangChain**, **OpenAI API**, and **Streamlit**.  
Upload one or more PDFs, the app extracts their text, splits it into manageable chunks, builds a **FAISS** vector index, and lets you ask question with conversational memory.

**Key features**
- PDF text extraction via `PyPDF2`
- Line‑aware chunking with **CharacterTextSplitter** 
- **FAISS** vector store for fast similarity search
- **OpenAIEmbeddings** + **ChatOpenAI** for high‑quality answers
- **ConversationalRetrievalChain** with **ConversationBufferMemory** to keep chat context
- Simple, clean **Streamlit** UI 

---

## 🧱 Architecture
```
PDFs → PyPDF2 (text) → text chunks → GPT(Word Embeddings) → FAISS (vector store)
Similarity Search → Conversation Chain (ChatOpenAI + Memory) → Streamlit UI
```

## ⚙️ Requirements
- Python **3.10** (recommended)
- An **OpenAI API key**

### Python dependencies (pip)
```
streamlit
langchain
openai
faiss-cpu
PyPDF2
python-dotenv
tiktoken
```

You can install them directly:
```bash
pip install streamlit langchain openai faiss-cpu PyPDF2 python-dotenv tiktoken
```

## 🔐 Environment Variables
The app uses `python-dotenv` to load your API key from a `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
```

- Put this `.env` file in the project root (same folder as `main.py`).

---

## 🏃 Run the App
From the project folder:
```bash
streamlit run main.py
```

**Workflow in the UI**
1. Use the sidebar to **upload one or more PDFs**.
2. Click **“Process PDFs”** – the app will extract text, chunk it, embed it, and build the FAISS vector store.
3. Ask questions in the text box (Ex: “Summarize chapter 2”).
4. You will Receive answers within seconds.

---

