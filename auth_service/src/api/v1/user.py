from fastapi import APIRouter, Depends, status

from src.schemas.user import UserInDB, UserCreate
from src.services.user import UserService

router = APIRouter(tags=["user"])


@router.post("/signup", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_create: UserCreate, service: UserService = Depends(UserService)
) -> UserInDB:
    return await service.register(user_create)
