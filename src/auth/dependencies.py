from typing import Any
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from .utils import decode_token
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from src.db.redis import jti_in_token_blocklist
from src.db.main import get_session
from .services import UserService
from src.db.models import User
from src.errors import(
    InvalidToken,
    AccessTokenRequired,
    RefreshTokenRequired,
    InsufficientPermission,
    AccountNotVerified
)


user_service=UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)
        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken() 
            # HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail={"error":"Invalid or expired token",
            #     "resolution":"Please create a new token"
            #     }
            # )
        
        if await jti_in_token_blocklist(token_data["jti"]):
           raise InvalidToken()  
        # HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail={"error": "This token has been revoked or expired",
        #         "resolution": "Please create a new token"
        #         }
        #     )

        self.verify_token_data(token_data)
    
        return token_data
    
    def verify_token_data(self,token_data):
        raise NotImplementedError("Please override this method in the child classes")

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self,token_data):
        if token_data and token_data.get("refresh"):
            raise AccessTokenRequired()
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail="Please provide an access token"
            # )

class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self,token_data):
        if token_data and not token_data.get("refresh"):
           raise RefreshTokenRequired()
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail="Please provide an refresh token"
            # )

async def current_user(token_detail:dict=Depends(AccessTokenBearer()),session:AsyncSession=Depends(get_session)):
    email=token_detail["user"]["email"]

    user=await user_service.get_user_by_email(email,session)

    return user

class RoleChecker:
    def __init__(self,allowed_roles:List[str])->None:
        self.allowed_roles=allowed_roles
    
    def __call__(self,current_user:User=Depends(current_user))->Any:
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()

        
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={
        #     "error":"You are not permitted for this route"
        # })

