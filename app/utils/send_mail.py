from fastapi import (
    FastAPI, 
    BackgroundTasks, 
    UploadFile, File, 
    Form, 
    Query,
    Body,
    Depends
)
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List
from fastapi_mail.email_utils import DefaultChecker

class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "YourUsername",
    MAIL_PASSWORD = "strong_password",
    MAIL_FROM = "your@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "your mail server",
    MAIL_FROM_NAME="Desired Name",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)