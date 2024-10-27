
from fastapi import APIRouter, HTTPException
from mako.compat import win32

from passlib.context import CryptContext

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    async with async_session_maker() as session:
        registered_user = await UsersRepository(session).get_one_or_none(email=data.email)

        if registered_user is not None:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = pwd_context.hash(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}