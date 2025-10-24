from sqlalchemy.orm import Session
from . import models

def create_file_record(db: Session, original_filename: str, system_filename: str, file_size: int):
    record = models.FileRecord(
        original_filename=original_filename,
        system_filename=system_filename,
        file_size_bytes=file_size
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_files(db: Session):
    return db.query(models.FileRecord).order_by(models.FileRecord.uploaded_at.desc()).all()
