import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.config_loader import conf
from common.logger import i, ex
from common.db import init_db
from routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    start()
    yield
    exit()


app = FastAPI(
    title=conf("title"),
    version=conf("version"),
    docs_url=None,
    redoc_url=None,
    root_path=f"/{conf('env')}",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=conf("allow_origins"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)


def start():
    i("Starting...")
    init_db()


def exit():
    i("Exiting...")


if __name__ == "__main__":
    port = conf("port")
    ssl_key_path = conf("ssl.key_path")
    ssl_cert_path = conf("ssl.cert_path")

    logger_conf = conf("logger")
    
    try:
        if ssl_key_path:
            uvicorn.run("main:app", host="0.0.0.0", port=port, ssl_keyfile=ssl_key_path, ssl_certfile=ssl_cert_path, log_config=logger_conf)
        else:
            uvicorn.run("main:app", host="127.0.0.1", port=port, log_config=logger_conf)
    except KeyboardInterrupt as ke:
        pass
    except Exception as e:
        ex(e)
