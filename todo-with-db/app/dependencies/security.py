from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.security import decode_access_token

bearer = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    token = credentials.credentials
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    try:
        token_data: dict[str, Any] = decode_access_token(token)
        user_id: str = token_data.get("sub")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    user = await UserRepository(db).get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    password_changed_at = user.password_changed_at

    if password_changed_at is not None:
        token_issued_at = datetime.fromtimestamp(token_data["iat"], tz=UTC)

        if token_issued_at <= password_changed_at:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
