from sqlalchemy.orm import Session
from src.entity.models import QueryHistory, DocumentText
from datetime import datetime
from typing import Optional, List


# Функція для створення запису в історії запитів
def create_query_history(db: Session, user_id: int, document_id: Optional[int], query: str, response: str) -> QueryHistory:
    new_query = QueryHistory(
        user_id=user_id,
        document_id=document_id,
        query=query,
        response=response,
        timestamp=datetime.utcnow()
    )
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query


# Функція для отримання історії запитів користувача
def get_user_query_history(db: Session, user_id: int) -> List[QueryHistory]:
    return db.query(QueryHistory).filter(QueryHistory.user_id == user_id).all()


# Функція для видалення запису з історії запитів
def delete_query_history(db: Session, query_id: int, user_id: int) -> bool:
    query = db.query(QueryHistory).filter(QueryHistory.id == query_id, QueryHistory.user_id == user_id).first()
    if query:
        db.delete(query)
        db.commit()
        return True
    return False


# Функція для отримання історії запитів користувача в залежності від користувача та документу
def get_user_query_history_by_doc(db: Session, user_id: int, filename: str) -> List[QueryHistory]:
    return db.query(QueryHistory).join(QueryHistory.document).filter(
        QueryHistory.user_id == user_id,
        DocumentText.filename == filename
    ).order_by(QueryHistory.timestamp).all()