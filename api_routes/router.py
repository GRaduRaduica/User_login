from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud_operation_models import get_user_by_username as crud_get_username
from db.crud_operation_models import create_user_profile as crud_create_user_profile
from skeletons.fastapi_app_schemas import UserFastapi, CreateUserFastapi
from db.db_config import db_sesh


router = APIRouter(prefix="/home", tags=['Users'])


@router.get("/user/{username}",
            response_model=UserFastapi,
            response_description="Get current user",
            status_code=status.HTTP_200_OK)
async def get_user_by_id(session: AsyncSession = Depends(db_sesh), username: str = None):

    user = await crud_get_username(session, username=username)

    if 'not_existent' in user:
        raise HTTPException(status_code=401,
                            detail=f"{username} is not registered yet")
    if not user:
        raise HTTPException(status_code=401,
                            detail=f"{username} not found")

    return user


@router.post("/create_user",
             response_description="Create new user",
             status_code=status.HTTP_201_CREATED)
async def create_user_profile(payload: CreateUserFastapi,
                              session: AsyncSession = Depends(db_sesh)):

    create_user = await crud_create_user_profile(session,
                                                 payload.username,
                                                 payload.password,
                                                 payload.email,
                                                 payload.phone_no)
    return {
        "id": create_user.id,
        "username": create_user.username
    }


@router.post("/login")
async def login_user(payload: CreateUserFastapi,
                     session: AsyncSession = Depends(db_sesh)):

    registered_user = await crud_get_username(session=session, username=payload.username)
    if 'not_existent' in registered_user:
        raise HTTPException(status_code=401,
                            detail=f"{payload.username} is not registered yet")
    if not registered_user:
        raise HTTPException(status_code=401,
                            detail=f"{payload.username} not found")

    if registered_user.password != payload.password:
        raise HTTPException(status_code=401,
                            detail=r"User/password not valid")

    return {
        "message": "Login successful",
    }
