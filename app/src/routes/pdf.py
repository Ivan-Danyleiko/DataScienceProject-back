from datetime import datetime
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from src.pdf_processing import extract_text_from_pdf
from src.database.db import get_db
from src.entity.models import DocumentText, QueryHistory, User
from src.services.auth import auth_service
import os
from src.services.model import process_text


router = APIRouter(prefix="/pdf",tags=["PDF Upload"])


@router.post("/upload-pdf/")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):

    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Only PDF files are allowed")

    content = await file.read()
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, 'wb') as f:
        f.write(content)

    try:
        text = extract_text_from_pdf(temp_file_path)
        if not text:
            raise ValueError(
                "Extracted text is empty. Please check the PDF content.")

        document = DocumentText(user_id=current_user.id,
                                filename=file.filename, text=text)
        db.add(document)
        db.commit()

        return {"message": "PDF processed and saved successfully", "text_sample": text[:2000]}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing PDF: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)





#############################################################################

### заглушка для роботи з LLM приймае і док-т і питання   вона відпрацювала добре, поки не використовую
# @router.post("/upload_new_pdf/")
# async def upload_new_pdf(
#     current_user: User = Depends(auth_service.get_current_user),
#     # request: Request,
#     text: str = Form(...),
#     # description: str = Form(...),
# ):

#     # ansver_text = process_text(text, description)
#     # return ansver_text
#     return None





@router.post("/upload_new_pdf_test/")
async def upload_new_pdf_test(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
    text: str = Form(...),
    description: str = Form(...),
):
    new_document = DocumentText(
        user_id=current_user.id,
        filename=description,
        text=text
    )
    db.add(new_document)
    db.commit()
    return current_user





@router.post("/request_for_title_docs/")
async def request_for_title_docs(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    name_documents = db.query(DocumentText.filename).filter(
        DocumentText.user_id == current_user.id).all()
    name_documents = [doc.filename for doc in name_documents]
    return name_documents





@router.post("/request_for_logs/")
async def request_for_logs(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
    document: str = Form(...),
):
    document_logs = db.query(QueryHistory).filter(
        QueryHistory.user_id == current_user.id,
        QueryHistory.document_name == document
    ).all()
    document_content = [(log.question, log.answer) for log in document_logs]
    return document_content





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

    new_query_history = QueryHistory(
        user_id=current_user.id,
        document_id=document_record.id,
        query=question,
        response=answer_text,
        timestamp=datetime.utcnow()
    )
    db.add(new_query_history)
    db.commit()

    return answer_text
