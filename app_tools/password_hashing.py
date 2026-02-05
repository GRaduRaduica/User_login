from fastapi.concurrency import run_in_threadpool
# from passlib.context import CryptContext
import bcrypt

# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # return await run_in_threadpool(pwd_context.hash, password)


