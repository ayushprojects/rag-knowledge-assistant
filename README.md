# Enterprise RAG Knowledge Assistant

A document Q&A app. Upload PDF or Markdown files, then ask questions in a chat UI. Answers are generated only from your documents using Retrieval-Augmented Generation (RAG), and each answer shows its sources.

## How it works

```
UPLOAD (once per file)
 PDF / Markdown -> text -> chunks -> embeddings -> Pinecone

ASK (every question)
 Question -> embedding -> Pinecone top-k chunks -> prompt (context + question) -> LLM -> answer + sources
```

1. **Ingestion:** the file is read, split into 500-character chunks (50 overlap), converted to 384-dimension vectors, and stored in Pinecone with the text, file name and page number.
2. **Retrieval:** the question is embedded with the same model and the 3 most similar chunks are fetched.
3. **Generation:** the chunks are put in a prompt that tells the LLM to answer only from the context. If the answer is not there, it says so. This reduces hallucinations.

## Tech stack

| Part            | Tool                                                                |
| --------------- | ------------------------------------------------------------------- |
| Backend         | Python, FastAPI                                                     |
| RAG framework   | LangChain                                                           |
| Embeddings      | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (runs locally) |
| Vector database | Pinecone (serverless, cosine, 384 dimensions)                       |
| LLM             | Groq API (chat model set in `.env`)                                 |
| Frontend        | React (Vite)                                                        |

## Project structure

```
rag-knowledge-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py         # FastAPI app and endpoints
│   │   ├── config.py       # settings loaded from .env
│   │   ├── clients.py      # embedding model, Pinecone index, LLM
│   │   ├── ingestion.py    # load -> chunk -> embed -> upsert
│   │   ├── retrieval.py    # question -> top-k chunks
│   │   ├── rag_chain.py    # prompt + LLM + sources
│   │   └── schemas.py      # request/response models
│   ├── create_index.py     # one-time Pinecone index creation
│   └── requirements.txt
└── frontend/               # React chat UI
```

## API endpoints

| Method | Path      | Purpose                                                                    |
| ------ | --------- | -------------------------------------------------------------------------- |
| GET    | `/health` | Health check                                                               |
| POST   | `/upload` | Upload a `.pdf` or `.md` file and store it in Pinecone                     |
| POST   | `/ask`    | Body: `{"question": "..."}`. Returns `{"answer": "...", "sources": [...]}` |

Interactive docs are available at `http://127.0.0.1:8000/docs`.

## Setup

### Prerequisites

- Python 3.10+
- Node.js 20+
- A free [Groq](https://console.groq.com) API key
- A free [Pinecone](https://www.pinecone.io) API key

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env`:

```
GROQ_API_KEY=your_groq_key
GROQ_MODEL=your_groq_chat_model_name
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=rag-knowledge-assistant
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
```

Create the Pinecone index (once), then start the server:

```bash
python create_index.py
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. The first start takes a few seconds because the embedding model is loaded (downloaded on first use).

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Usage

1. Click **Choose File** and upload a PDF or Markdown file.
2. Wait for the "chunks stored" message.
3. Ask a question in the chat box. The answer appears with its sources (file and page).

## Limitations

- English works best. The embedding model is English-focused.
- Scanned PDFs (images without text) are not supported, there is no OCR.
- Markdown files are treated as a single "page".

## Future improvements

- Multilingual embedding model
- OCR for scanned PDFs
- Per-user document spaces using Pinecone namespaces
- Streaming answers
