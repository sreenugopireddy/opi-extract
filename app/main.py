import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="OptiExtract - File Uploader")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-document", response_model=schemas.FileRecordOut)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    original_filename = file.filename
    ext = os.path.splitext(original_filename)[1] or ""
    system_filename = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, system_filename)

    try:
        with open(dest_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                buffer.write(chunk)
    except Exception as e:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    file_size = os.path.getsize(dest_path)

    try:
        record = crud.create_file_record(db, original_filename, system_filename, file_size)
    except Exception as e:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        raise HTTPException(status_code=500, detail=f"Failed to record metadata: {e}")

    return record

@app.get("/files", response_model=list[schemas.FileRecordOut])
def list_files(db: Session = Depends(get_db)):
    return crud.get_all_files(db)

@app.get("/", response_class=HTMLResponse)
def upload_page():
    with open("templates/upload.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/history", response_class=HTMLResponse)
def history_page():
    with open("templates/files.html", "r", encoding="utf-8") as f:
        return f.read()
