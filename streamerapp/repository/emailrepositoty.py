from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl
import tempfile
from typing import Any, Dict, List
import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.config import EmailConfig

from .. import models, schemas 
from email import encoders



async def sendemail(from_email:str,to_email:str,subject:str,message:str,is_urgent:bool,timestamp:str,attachments):
    try:
        # Generate unique message ID
        message_id = str(uuid.uuid4())
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EmailConfig.EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = f"[URGENT] {subject}" if is_urgent else subject
        msg['Reply-To'] = from_email
        
        # Add custom headers
        msg['X-Priority'] = '1' if is_urgent else '3'
        msg['X-MSMail-Priority'] = 'High' if is_urgent else 'Normal'
        msg['Message-ID'] = f"<{message_id}@yourdomain.com>"
        
        # Email body with sender info
        email_body = f"""
Original Sender: {from_email}
Sent: {timestamp}
Priority: {'HIGH' if is_urgent else 'NORMAL'}

---

{message}

---
This email was sent through the Tank Monitoring System.
Please reply directly to: {from_email}
        """
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        # Handle attachments
        temp_files = []
        if attachments:
            for attachment in attachments:
                if attachment.filename:
                    # Create temporary file
                    temp_file = tempfile.NamedTemporaryFile(delete=False)
                    temp_files.append(temp_file.name)
                    
                    # Write uploaded file to temp file
                    content = await attachment.read()
                    temp_file.write(content)
                    temp_file.close()
                    
                    # Attach to email
                    with open(temp_file.name, "rb") as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {attachment.filename}',
                    )
                    msg.attach(part)
        
        # Send email
        context = ssl.create_default_context()
        
        with smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EmailConfig.EMAIL_ADDRESS, EmailConfig.EMAIL_PASSWORD)
            
            text = msg.as_string()
            server.sendmail(EmailConfig.EMAIL_ADDRESS, to_email, text)
        
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        return schemas.EmailResponse(
            success=True,
            message="Email sent successfully",
            messageId=message_id
        )
        
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="Email authentication failed. Check credentials."
        )
    except smtplib.SMTPRecipientsRefused:
        raise HTTPException(
            status_code=400,
            detail="Invalid recipient email address."
        )
    except smtplib.SMTPServerDisconnected:
        raise HTTPException(
            status_code=503,
            detail="Email server connection lost. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )
        
async def sendsimpleemail(email_data:schemas.EmailRequest):      
    try:
        message_id = str(uuid.uuid4())
        
        msg = MIMEMultipart()
        msg['From'] = EmailConfig.EMAIL_ADDRESS
        msg['To'] = email_data.to_email
        msg['Subject'] = f"[URGENT] {email_data.subject}" if email_data.is_urgent else email_data.subject
        msg['Reply-To'] = email_data.from_email
        msg['Message-ID'] = f"<{message_id}@yourdomain.com>"
        
        # Priority headers
        if email_data.is_urgent:
            msg['X-Priority'] = '1'
            msg['X-MSMail-Priority'] = 'High'
        
        email_body = f"""
Original Sender: {email_data.from_email}
Sent: {datetime.now().isoformat()}
Priority: {'HIGH' if email_data.is_urgent else 'NORMAL'}

---

{email_data.message}

---
This email was sent through the Tank Monitoring System.
Please reply directly to: {email_data.from_email}
        """
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EmailConfig.EMAIL_ADDRESS, EmailConfig.EMAIL_PASSWORD)
            server.sendmail(EmailConfig.EMAIL_ADDRESS, email_data.to_email, msg.as_string())
        
        return schemas.EmailResponse(
            success=True,
            message="Email sent successfully",
            messageId=message_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  