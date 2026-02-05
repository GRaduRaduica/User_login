from sqlalchemy.ext.asyncio import AsyncSession
from db.crud_operation_models import get_user_by_email as crud_get_email
from skeletons.db_schemas import CreatedUserDB
from app_tools.security import verify_password
from app_tools.jwt import create_access_token


async def authenticate_user(session_db: AsyncSession, email: str, password: str) -> str | None:

    result = crud_get_email(session_db, email)

    if not result:
        return None

    if not await verify_password(password, result.hashed_password):
        return None

    return create_access_token(str(result.id))
