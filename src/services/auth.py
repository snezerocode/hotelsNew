import jwt
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, Response

from src.api.dependencies import UserIdDep
from src.config import settings
from passlib.context import CryptContext

from src.exceptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotFoundException,
    WrongPasswordException,
)
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")

    async def register_user(
        self,
        data: UserRequestAdd,
    ):
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsHTTPException

    async def login_user(self, data: UserRequestAdd, response: Response):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotFoundException
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise WrongPasswordException
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return access_token

    async def logout(self, response: Response):
        response.delete_cookie("access_token")

    async def get_me(self, user_id: UserIdDep):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user
