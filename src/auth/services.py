

from .utils import generate_password_hash
from .schema import UserCreate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
class UserService:
    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement=select(User).where(User.email==email)
        result=await session.exec(statement)
        return result.first()

    async def user_exists(self,email:str,session:AsyncSession):
        user =await self.get_user_by_email(email,session)

        return True if user is not None else False
    
    async def create_user(self, create_user: UserCreate, session: AsyncSession):
        user = create_user.model_dump(exclude={"password"})
        new_user = User(**user)
        new_user.password_hash = generate_password_hash(create_user.password)
        new_user.role="user"
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def update_user(self,user:User,user_data:dict,session: AsyncSession):
        for k,v in user_data.items():
            setattr(user,k,v)
        await session.commit()

        return user
