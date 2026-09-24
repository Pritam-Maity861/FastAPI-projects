from fastapi import HTTPException, status
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
)



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

    async def login(self, data: UserLogin) -> UserResponse:
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
        return TokenResponse(access_token=access_token)


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
