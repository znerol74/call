from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, agents, phone_numbers, calls, gdpr, tools, testing, twilio_webhook


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="CAL - AI Phone Agent System",
    description="Multi-tenant GDPR-compliant AI phone agent assistant",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(phone_numbers.router, prefix="/api/v1/phone-numbers", tags=["Phone Numbers"])
app.include_router(calls.router, prefix="/api/v1/calls", tags=["Calls"])
app.include_router(gdpr.router, prefix="/api/v1/gdpr", tags=["GDPR"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["Tools"])
app.include_router(testing.router, prefix="/api/v1/testing", tags=["Testing"])
app.include_router(twilio_webhook.router, prefix="/api/v1/twilio", tags=["Twilio Webhooks"])


@app.get("/")
async def root():
    return {"message": "CAL API - AI Phone Agent System", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
