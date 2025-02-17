from sqlalchemy.orm import Session
from fastapi import UploadFile
import os
from datetime import datetime

from app.models.template import Template
from app.schemas.template import TemplateCreate

async def create_template(db: Session, file: UploadFile, user_id: int) -> Template:
    # Создаем директорию для файлов, если её нет
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Генерируем уникальное имя файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"{upload_dir}/{timestamp}_{file.filename}"
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Создаем запись в БД
    db_template = Template(
        filename=file.filename,
        file_path=file_path,
        content_type=file.content_type,
        user_id=user_id
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def get_templates(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Template)\
        .filter(Template.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_template(db: Session, template_id: int):
    return db.query(Template).filter(Template.id == template_id).first()

def delete_template(db: Session, template_id: int):
    template = get_template(db, template_id)
    if template and os.path.exists(template.file_path):
        os.remove(template.file_path)
    db.delete(template)
    db.commit()
    return template
