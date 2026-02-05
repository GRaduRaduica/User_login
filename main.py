from fastapi import FastAPI
from api_routes.router import router
# from app_tools.LogHandler import LogStorageHandler, LogLevel
# from pathlib import Path

# TODO: add logging for each important event
# WORKING_DIR = Path(__file__).parent / "logs"
# log_file = WORKING_DIR / 'mainLogs.log'
#
# logs = LogStorageHandler(logfile=log_file, maxBytes=1024 * 4, backupCount=1)
# logs.setLevel(LogLevel.INFO)
# logs.info("I'm up and running!")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     #bootup_func()
#     yield


app = FastAPI()

app.include_router(router=router)
