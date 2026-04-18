from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes.auth import router as auth_router
from app.routes.resume import router as resume_router
from app.jd.routes import router as jd_router
from app.config.settings import settings
from app.config.database import engine, Base


app = FastAPI(
    title="ATS Resume Optimizer Backend",
    version="0.1.0",
    description="Authentication service for ATS Resume Optimizer.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@app.exception_handler(ValueError)
async def value_error_exception_handler(_, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(resume_router, prefix="/resume", tags=["resume"])
app.include_router(jd_router, prefix="/jd", tags=["jd"])
