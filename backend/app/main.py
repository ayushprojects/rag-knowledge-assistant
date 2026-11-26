import os
import shutil
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, HTTPException, UploadFile

from app.ingestion import ingest_file
from app.rag_chain import answer_question
from app.schemas import AskRequest, AskResponse

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="Enterprise RAG Knowledge Assistant",
    description="Upload documents and ask questions answered from them.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "RAG Knowledge Assistant API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in (".pdf", ".md"):
        raise HTTPException(status_code=400, detail="Only .pdf and .md files are supported")

    save_path = os.path.join(UPLOAD_DIR, os.path.basename(file.filename))
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks_stored = ingest_file(save_path)
    if chunks_stored == 0:
        raise HTTPException(status_code=422, detail="No text could be extracted from this file")

    return {"filename": file.filename, "chunks_stored": chunks_stored}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return answer_question(request.question)