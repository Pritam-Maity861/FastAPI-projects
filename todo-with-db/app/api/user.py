from fastapi import APIRouter,Depends,status,Response,Cookie

from app.dependencies.user import get_user_service
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.schemas.user import TokenResponse,UserLogin,UserResponse
from app.dependencies.security import CurrentUser 



userRouter = APIRouter(prefix="/user", tags=["user"])


@userRouter.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate,
    userService: UserService = Depends(get_user_service),
):
    user = await userService.register(payload)
    return user

@userRouter.post("/login",response_model=TokenResponse)
async def login(
    payload:UserLogin,
    response: Response, 
    userService:UserService=Depends(get_user_service)
):
    return await userService.login(payload,response=response)


@userRouter.post("/get-by-id/{user_id}",response_model=UserResponse)
async def get_user_by_id(
    user_id:str,
    userService:UserService=Depends(get_user_service)
):
    return await userService.get_user_by_id(user_id)


@userRouter.post("/refresh-access-token")
async def refresh_access_token(
    response: Response,
    refresh_token: str = Cookie(None),
    userService:UserService=Depends(get_user_service)
): 
    return await userService.refresh_session(refresh_token,response=response)


@userRouter.get("/me",response_model=UserResponse)
async def get_me(user:CurrentUser):
    return user   