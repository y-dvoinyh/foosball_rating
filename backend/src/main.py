import uvicorn
from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(
        # title=settings.PROJECT_NAME,
        # debug=settings.DEBUG,
        # version=settings.VERSION
    )
    #application.include_router(get_apps_router())


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
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
