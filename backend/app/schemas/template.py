from datetime import datetime
from pydantic import BaseModel

class TemplateBase(BaseModel):
    filename: str
    content_type: str

class TemplateCreate(TemplateBase):
    pass

class Template(TemplateBase):
    id: int
    file_path: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
