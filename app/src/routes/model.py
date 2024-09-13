from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.entity.models import DocumentText, QueryHistory, User
from src.services.auth import auth_service
from src.services.model import process_text
from src.repository import query_history as repository


router = APIRouter(prefix="/model",tags=["Model"])



@router.post("/ask_question/")
async def ask_question(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
    document: str = Form(...),
    question: str = Form(...),
):
    document_record = db.query(DocumentText).filter(
        DocumentText.user_id == current_user.id,
        DocumentText.filename == document
    ).first()

    if not document_record:
        raise HTTPException(status_code=404, detail="Document not found")
    
    answer_text = process_text(document_record.text, question)

    new_query = repository.create_query_history(
        db=db,
        user_id=current_user.id,
        document_id=document_record.id,
        query=question,
        response=answer_text
    )

    if not new_query:
        raise HTTPException(status_code=404, detail="Query dont create")
    
    answer_text = process_text(document_record.text, question)

    # new_query_history = QueryHistory(
    #     user_id=current_user.id,
    #     document_id=document_record.id,
    #     query=question,
    #     response=answer_text,
    #     timestamp=datetime.utcnow()
    # )
    # db.add(new_query_history)
    # db.commit()

    return answer_text
