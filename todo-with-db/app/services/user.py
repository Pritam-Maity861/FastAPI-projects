from typing import Any
from fastapi import HTTPException, status, Response, Cookie, HTTPException
from app.repositories.user import UserRepository
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse,
)
from app.models.user import User
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_refresh_token,
    decode_refresh_token,
)

from datetime import timedelta


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreate) -> UserResponse:
        existing = await self.repo.get_by_email(data.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="email already exist."
            )

        password_hash = hash_password(data.password)
        user = User(
            email=data.email, hash_password=password_hash, full_name=data.full_name
        )
        created_user = await self.repo.create(user)
        return UserResponse.model_validate(created_user)

    async def get_user_by_id(self, user_id) -> UserResponse:
        user = await self.repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return UserResponse.model_validate(user)

    async def login(self, data: UserLogin, response: Response) -> TokenResponse:
        user = await self.repo.get_by_email(data.email)
        if user is None or not verify_password(data.password, user.hash_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        access_token = create_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)

        refresh_lifetime = timedelta(days=7)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=int(refresh_lifetime.total_seconds()),
            httponly=True,
            samesite="lax",
            secure=False,
        )

        return TokenResponse(access_token=access_token)

    async def refresh_session(self, refresh_token: str,response: Response)->TokenResponse:
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token missing")

        try:
            token_data: dict[str, Any] = decode_refresh_token(refresh_token)
            user_id: str = token_data.get("sub")

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )
        
        user=await self.repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")

        new_access_token = create_access_token(user.id)
        new_refresh_token = generate_refresh_token(user.id)

        refresh_lifetime = timedelta(days=7)

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            max_age=int(refresh_lifetime.total_seconds()),
            httponly=True,
            samesite="lax",
            secure=False,
        )

        return TokenResponse(access_token=new_access_token)
    



    # async def update_user(self, user_id: uuid.UUID, data: UserUpdate) -> UserResponse:
    #     user = await self.repo.get_by_id(user_id)

    #     if user is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="User not found.",
    #         )

    #     update_data = data.model_dump(exclude_unset=True)

    #     for field, value in update_data.items():
    #         setattr(user, field, value)

    #     try:
    #         updated_user = await self.repo.update(user)
    #     except:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT, detail="Email already exists."
    #         )

    #     return UserResponse.model_validate(updated_user)
