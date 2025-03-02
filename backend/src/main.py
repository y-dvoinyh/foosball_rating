from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.models import db_helper
from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def get_application() -> FastAPI:
    application = FastAPI(
        # title=settings.PROJECT_NAME,
        # debug=settings.DEBUG,
        # version=settings.VERSION
        lifespan=lifespan
    )
    application.include_router(api_router, prefix=settings.api.prefix)

    # application.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=settings.CORS_ALLOWED_ORIGINS.split(" "),
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )
    return application


main_app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
