from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from typing import Annotated,Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException,status
from app.db.database import get_db
from app.security import decode_access_token
from app.repositories.user import UserRepository
from app.models.user import User


bearer = HTTPBearer()

async def get_current_user(
        credentials:Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
        db:Annotated[AsyncSession,Depends(get_db)]
):
    token=credentials.credentials
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    
    try:
        token_data:dict[str,Any]=decode_access_token(token)
        user_id:str = token_data.get("sub")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    
    user=await UserRepository(db).get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")

    return user



CurrentUser=Annotated[User,Depends(get_current_user)]