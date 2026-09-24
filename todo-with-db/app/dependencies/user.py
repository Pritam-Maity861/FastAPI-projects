from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from typing import Annotated
from fastapi import Depends
from app.repositories.user import UserRepository
from app.services.user import UserService



def get_user_service(db_session:Annotated[AsyncSession,Depends(get_db)]):
    repo=UserRepository(db=db_session)
    return UserService(repo)

userServiceDependency=Annotated[UserService,Depends(get_user_service)]



    