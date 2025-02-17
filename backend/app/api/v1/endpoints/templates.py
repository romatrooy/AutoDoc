from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.crud import template as crud
from app.db.database import get_db
from app.schemas.template import Template
from app.api.deps import get_current_user
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=Template)
async def create_template(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crud.create_template(db=db, file=file, user_id=current_user.id)

@router.get("/", response_model=List[Template])
def read_templates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    templates = crud.get_templates(db, user_id=current_user.id, skip=skip, limit=limit)
    return templates

@router.get("/{template_id}", response_model=Template)
def read_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    template = crud.get_template(db, template_id=template_id)
    if template is None or template.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.delete("/{template_id}", response_model=Template)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    template = crud.get_template(db, template_id=template_id)
    if template is None or template.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Template not found")
    return crud.delete_template(db=db, template_id=template_id)
