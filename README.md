# 📚 Multi‑PDF Chatbot with LangChain & Streamlit and deploying using AWS EC2

## 📌 Overview
This project is an interactive **PDF Q&A chatbot** built with **LangChain**, **OpenAI API**, and **Streamlit**.  
Upload one or more PDFs, the app extracts their text, splits it into manageable chunks, builds a **FAISS** vector index, and lets you ask question with conversational memory.

**Key features**
- PDF text extraction via `PyPDF2`
- Line‑aware chunking with **CharacterTextSplitter** 
- **FAISS** vector library for fast similarity search
- **OpenAIEmbeddings** + **ChatOpenAI** for high‑quality answers
- **ConversationalRetrievalChain** with **ConversationBufferMemory** to keep chat context
- Simple, clean **Streamlit** UI 

---

## 🧱 Architecture
```
PDFs → single text → text chunks → Word Embeddings → FAISS vector library → Conversation Chain
```
## 📂 Conversational Chain Flow

```text
Question
   ↓
Word Embedding
   ↓
Semantic Search (FAISS)
   ↓
Ranked Results
   ↓
Text Chunks ──────→ LLM ──────→ Answer
```

---
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


**Workflow in the UI**
1. Use the sidebar to **upload one or more PDFs**.
2. Click **“Process PDFs”** – the app will extract text, chunk it, embed it, and build the FAISS vector store.
3. Ask questions in the text box (Ex: “Summarize chapter 2”).
4. You will Receive answers within seconds.

---
## 🔧 Deployment Process

### 1. Connect to EC2 Instance
Use SSH to connect to your running EC2 instance:
```bash
ssh -i "langchain.pem" ec2-user@ec2-3-108-220-64.ap-south-1.compute.amazonaws.com
```

### 2. Create & Activate Virtual Environment
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Copy Files to EC2
From your **local machine**, upload the project files:
```bash
scp -i "langchain.pem" app.py htmlTemplates.py requirements.txt .env ec2-user@ec2-3-108-220-64.ap-south-1.compute.amazonaws.com:/home/ec2-user/
```

### 4. Install Dependencies
Inside the EC2 instance:
```bash
pip install -r requirements.txt
```

### 6. Run in Background (Optional)
To keep it running after disconnecting SSH:
```bash
nohup streamlit run app.py &
```
---

## 🌍 Access the App
Once running, open the app in your browser:  
```
http://3.108.220.64:8501/
```
