# from fastapi import FastAPI
# from src.infrastructure.logging.logger import configure_logging
# from api.routers import auth_router,user_router
# from src.infrastructure.general.db import Base,engine
# from scalar_fastapi import get_scalar_api_reference

# configure_logging()
# Base.metadata.create_all(bind=engine)
# app = FastAPI()

# app.include_router(auth_router.router )
# app.include_router(user_router.router)

# @app.get("/")
# async def root():
#     return {"status": "ok"}

# @app.get("/health")
# async def health():
#     return {"status": "alive"}

# @app.get("/scalar" , include_in_schema = False)
# async def scalar():
#     return (
#         get_scalar_api_reference(
#             openapi_url = app.openapi_url
#             ,title= 'Scalar API'
#         )
#     )

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.infrastructure.logging.logger import configure_logging
from api.routers import auth_router, user_router
from src.infrastructure.general.db import Base, engine
from scalar_fastapi import get_scalar_api_reference
import logging

# تهيئة اللوجينج
configure_logging()
logger = logging.getLogger(__name__)

# محاولة إنشاء الجداول بطريقة آمنة
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")

# إنشاء التطبيق
app = FastAPI(title="Homney API")

# إضافة الروترات
app.include_router(auth_router.router)
app.include_router(user_router.router)

# Healthcheck الأساسي
@app.get("/")
async def root():
    return {"status": "ok"}

# Healthcheck مخصص لتجنب مشاكل DB
@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "alive"}

# Route لـ Scalar API
@app.get("/scalar", include_in_schema=False)
async def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title='Scalar API'
    )

# Logging عند بدء التطبيق
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")

# Logging عند إيقاف التطبيق
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown complete.")