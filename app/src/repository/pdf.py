from sqlalchemy.orm import Session
from src.entity.models import DocumentText, QueryHistory
from datetime import datetime
from typing import List, Optional


def save_new_document(db: Session, user_id: int, filename: str, text: str) -> Optional[DocumentText]:
    existing_document = db.query(DocumentText).filter(
        DocumentText.user_id == user_id,
        DocumentText.filename == filename
    ).first()
    if existing_document:
        return None

    new_document = DocumentText(
        user_id=user_id,
        filename=filename,
        text=text
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document


def get_document_titles(db: Session, user_id: int) -> List[str]:
    documents = db.query(DocumentText.filename).filter(DocumentText.user_id == user_id).all()
    return [doc.filename for doc in documents]


def get_query_history(db: Session, user_id: int, document_name: str) -> List[QueryHistory]:
    document_logs = db.query(QueryHistory).join(QueryHistory.document).filter(
        QueryHistory.user_id == user_id,
        DocumentText.filename == document_name
        ).all()
    return [(log.query, log.response) for log in document_logs]
