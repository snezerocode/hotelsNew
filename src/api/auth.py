from fastapi import APIRouter, Response

from src.exceptions import (
    UserNotFoundException,
    UserNotFoundHTTPException,
    WrongPasswordHTTPException,
    WrongPasswordException,
)
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    await AuthService(db).register_user(data)
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data, response)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except WrongPasswordException:
        raise WrongPasswordHTTPException
    return {"access_token": access_token}


@router.get("/logout")
async def logout(response: Response):
    await AuthService().logout(response)
    return {"status": "Bye Bye"}


@router.post("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await AuthService(db).get_me(user_id)
    return user
