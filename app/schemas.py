from pydantic import BaseModel
from datetime import datetime

class FileRecordOut(BaseModel):
    id: int
    original_filename: str
    system_filename: str
    file_size_bytes: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
