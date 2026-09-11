import logging
import uuid
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from src.config import getsetting
from itsdangerous import URLSafeTimedSerializer
set=getsetting()
AccessTokenTime=3600
def generate_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password_hash(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def create_access_token(user_data:dict, expire:timedelta=None,refresh:bool=False)->str:
    payload={}
    payload["user"]=user_data
    payload["exp"]=datetime.now(timezone.utc)+(
        expire if expire is not None else timedelta(seconds=AccessTokenTime)
        )
    payload["jti"]=str(uuid.uuid4())
    payload["refresh"]=refresh

    token=jwt.encode(
        payload=payload,
        key=set.JWT_KEY,
        algorithm=set.JWT_ALORITHM)

    return token

def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=set.JWT_KEY,
            algorithms=[set.JWT_ALORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

serialize=URLSafeTimedSerializer(secret_key=set.JWT_KEY,salt="email-verification")

def create_safe_url_token(data:dict):
    serialize_token=serialize.dumps(data)

    return serialize_token


def decode_safe_url_token(token:str):

    try:
        token_data=serialize.loads(token)

        return token_data
    except Exception as e:
        logging.exception(str(e))


    
    