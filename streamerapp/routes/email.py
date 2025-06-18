from fastapi import APIRouter, Depends, File, Form, UploadFile, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from streamerapp import oauth2
from streamerapp.repository import emailrepositoty, tankrepository 
from .. import schemas, database 



router = APIRouter(
    tags=['email'],
)


@router.post("/api/send-email", response_model=schemas.EmailResponse)
async def send_email(from_email: str = Form(...), to_email: str = Form(...),subject: str = Form(...), message: str = Form(...), is_urgent: bool = Form(False),
    timestamp: str = Form(...),attachments: Optional[List[UploadFile]] = File(None)):
    return await emailrepositoty.sendemail(from_email,to_email,subject,message,is_urgent,timestamp,attachments)

@router.post("/api/send-email-simple")
async def send_simple_email(email_data: schemas.EmailRequest):
    return await emailrepositoty.sendsimpleemail(email_data)