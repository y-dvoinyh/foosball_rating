import uvicorn
from fastapi import FastAPI

from core.config import settings
from api import router as api_router


def get_application() -> FastAPI:
    application = FastAPI(
        # title=settings.PROJECT_NAME,
        # debug=settings.DEBUG,
        # version=settings.VERSION
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


app = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
