from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    SECRET_KEY: str = r"jh-52uas874y781JEY32852J2uxu2($&8510=-..sjr28daslk2;.02jksj852jsOmw72mNS7@($"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = True

    config_file: dict = {
        "env_file": ".env"
    }


jwt_settings = JWTSettings()
