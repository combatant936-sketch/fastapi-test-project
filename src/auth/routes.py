from src.db.redis import add_jti_to_token_blocklist
from .dependencies import AccessTokenBearer
from datetime import datetime, timedelta, timezone
from .dependencies import RefreshTokenBearer
from fastapi.responses import JSONResponse
from .utils import create_access_token, verify_password_hash,create_safe_url_token,decode_safe_url_token,generate_password_hash
from .schema import UserLogin, UserCreate, UserModel,UserBookModel,EmailAddresses,PasswordResetRequest,PasswordResetConfirm
from fastapi import HTTPException, Depends, APIRouter, status,BackgroundTasks
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import UserService
from .dependencies import current_user,RoleChecker
from src.mail import mail,create_message
from src.config import getsetting
from src.celery_tasks import sent_email
settt=getsetting()


from src.errors import(
   UserAlreadyExists,
   UserNotFound,
   InvalidCredentials,
   InvalidToken
)

roleChecker=RoleChecker(["admin","user"])
userservice=UserService()
auth_routes=APIRouter()
AccessTokenDay=2

@auth_routes.post("/send-email")

async def send_email(emails:EmailAddresses):
    addresses=emails.addresses

    html="<h1>Welcome hello</h1>"
    # message=create_message(recipients=addresses,subject="Welcome",body=html)
    
    # await mail.send_message(message)
    sent_email.delay(["combatant936@gmail.com"],"Test Email",html)
    return {"message":"email send successfully"}




@auth_routes.post("/sign-up",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate,bg_tasks:BackgroundTasks,session:AsyncSession=Depends(get_session)):
    email=user.email

    user_exists=await userservice.user_exists(email,session)

    if user_exists:
        raise UserAlreadyExists() 
    # HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already exists")
    user = await userservice.create_user(user, session)

    token=create_safe_url_token({"email":email})

    link=f"http://{settt.DOMAIN}/api/v1/auth/verify-email/{token}"

    html=f"""<h1>verify your email</h1>
    <p>verify link {link}</p>
    """

    sent_email.delay([email],"Verify your email",html)

    # message=create_message(recipients=[email],subject="Verify your email",body=html)
    
    # bg_tasks.add_task(mail.send_message,message)


    return {
        "message":"new user create please verify the email email is send to this email",
        "user":user}


@auth_routes.get("/verify-email/{token}")
async def verify_email(token:str,session:AsyncSession=Depends(get_session)):
    token_data=decode_safe_url_token(token)

    if token_data:
        email=token_data.get("email")

        user =await userservice.get_user_by_email(email,session)

        if user:
            await userservice.update_user(user,{"is_verified":True},session)

            return JSONResponse(content={
                "message":"email verification is successfully"
                },status_code=status.HTTP_200_OK)
            
        else:
            raise UserNotFound()
    
    return JSONResponse(content={
        "message":"email verification is failed"
    },status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@auth_routes.post("/login")
async def login(user:UserLogin,session:AsyncSession=Depends(get_session)):
    email=user.email

    user_exists=await userservice.get_user_by_email(email,session)

    if user_exists is not None:
        password_verify=verify_password_hash(user.password,user_exists.password_hash)

        # return password_verify

        if password_verify:
            token=create_access_token(user_data={
                "uuid":str(user_exists.uuid),
                "email":user_exists.email,
                "role":user_exists.role
                })

            refresh_token=create_access_token(user_data={
                "uuid":str(user_exists.uuid),
                "email":user_exists.email,
                },expire=timedelta(days=AccessTokenDay),refresh=True)

            
            return JSONResponse(content={
                 "message": "Login successful",
                "access_token":token,
                "refresh_token":refresh_token,
                "user_data":{
                                "uuid":str(user_exists.uuid),
                    "email":user_exists.email,
       

                }
            })

        raise InvalidCredentials()


@auth_routes.get("/refresh-token")
async def get_new_refresh_token(token_detail:dict=Depends(RefreshTokenBearer())):
    expiry_timestamp = token_detail["exp"]
    if datetime.fromtimestamp(expiry_timestamp, tz=timezone.utc) > datetime.now(timezone.utc):
        new_token=create_access_token(user_data=token_detail["user"])

        return JSONResponse(content={
            "access_token":new_token
        })

    raise  InvalidToken()

# HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")


@auth_routes.get("/me",response_model=UserBookModel)
async def get_current_user(user:dict=Depends(current_user),_:bool=Depends(roleChecker)):
    return user

@auth_routes.post("/logout")
async def revoke_access_token(token_detail:dict=Depends(AccessTokenBearer())):
    jti=token_detail["jti"]

    await add_jti_to_token_blocklist(jti)

    return JSONResponse(content={
        "message":"Logged out successfully"

    },status_code=status.HTTP_200_OK)




@auth_routes.post("/password-reset-request")
async def password_reset_request(data:PasswordResetRequest,session:AsyncSession=Depends(get_session)):
        email=data.email

        user_exists=await userservice.user_exists(email,session)

        if not user_exists:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="user does not exist")

        token=create_safe_url_token({"email":email})

        link=f"http://{settt.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

        html=f"""<h1>password-reset-confirm</h1>
        <p>password-reset-confirm {link}</p>
        """

        sent_email.delay([email],"password-reset-confirm",html)
        # message=create_message(recipients=[email],subject="password-reset-confirm",body=html)
        
        # await mail.send_message(message)


        return JSONResponse(content={
            "message":"password-reset-confirm"}
            ,status_code=status.HTTP_200_OK
            
            )
@auth_routes.post("/password-reset-confirm/{token}")
async def password_reset_confirm(token:str,data:PasswordResetConfirm,session:AsyncSession=Depends(get_session)):
    token_data=decode_safe_url_token(token)

    new_password=data.new_password
    confirm_new_password=data.confirm_new_password

    if new_password != confirm_new_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password doest not match")



    if token_data:
        email=token_data.get("email")

        user =await userservice.get_user_by_email(email,session)

        if user:
            await userservice.update_user(user,{"password_hash":generate_password_hash(new_password)},session)

            return JSONResponse(content={
                "message":"password has been successfully reset"
                },status_code=status.HTTP_200_OK)
            
        else:
            raise UserNotFound()
    
    return JSONResponse(content={
        "message":"password reset is failed"
    },status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    


    

