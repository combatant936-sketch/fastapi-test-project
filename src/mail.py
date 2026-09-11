from typing import List
from fastapi_mail import FastMail,MessageSchema,MessageType,ConnectionConfig
from src.config import getsetting
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent
config=getsetting()

mail_config=ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME=config.MAIL_FROM_NAME,
    MAIL_STARTTLS=config.MAIL_STARTTLS,
    MAIL_SSL_TLS=config.MAIL_SSL_TLS,
    USE_CREDENTIALS=config.USE_CREDENTIALS,
    VALIDATE_CERTS=config.VALIDATE_CERTS,
    # TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)
mail=FastMail(config=mail_config)

def create_message(recipients:List[str],subject:str,body:str):
    message=MessageSchema(recipients=recipients,subject=subject,body=body,subtype=MessageType.html)

    return message
