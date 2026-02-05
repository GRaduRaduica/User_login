from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import ProgrammingError
from skeletons.db_schemas import UserDB, CreatedUserDB
from app_tools.password_hashing import hash_password

NON_EXISTENT = 'not_existent'


async def verify_table_existence(session: AsyncSession) -> bool:

    async with session.begin():
        try:
            await session.execute(select(UserDB).limit(1))
            return True
        except ProgrammingError:
            return False


async def get_user_by_username(session: AsyncSession, username: str) -> UserDB | None:

    if not await verify_table_existence(session):
        return NON_EXISTENT
    query = select(UserDB).where(UserDB.username == username)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> CreatedUserDB | None:

    if not await verify_table_existence(session):
        return NON_EXISTENT
    query = select(CreatedUserDB).where(CreatedUserDB.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_user_profile(session: AsyncSession,
                              username: str,
                              password: str,
                              email: str,
                              phone_no: str) -> UserDB:
    hashed_passw = hash_password(password)

    user = UserDB(username=username, password=hashed_passw)
    created_user = CreatedUserDB(email=email, phone_no=phone_no)
    session.add(user)
    session.add(created_user)
    await session.commit()
    await session.refresh(user)
    return user
