from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re


class UserFastapi(BaseModel):
    username: str = Field(alias='Username', min_length=4, max_length=35)
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, passw: str) -> str:
        if len(passw) < 8:
            raise ValueError("Password too short")

        if not re.search(r"[A-Z]", passw):
            raise ValueError("Password must contain an uppercase letter")

        if not re.search(r"\d", passw):
            raise ValueError("Password must contain a digit")

        if not re.search(r"[!@#$%^&*()_+=\-.,/]", passw):
            raise ValueError("Password must contain a special character")

        return passw


class CreateUserFastapi(UserFastapi):
    email: str
    phone_no: str
    date_created: str = datetime.now().ctime()


    @field_validator("phone_no")
    @classmethod
    def verify_phone_no(cls, num: str) -> str:

        if len(num) != 10:
            raise ValueError("Phone number must be 10 digits long")
        return num


    @field_validator("email")
    @classmethod
    def verify_email(cls, email: str) -> str:
        if "@" not in email:
            raise ValueError("Email format must contain '@'")
        return email
