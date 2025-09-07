import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ==== FastAPI app ====
app = FastAPI(
    title="IAM System API - DEBUG",
    description="Debug version to isolate 502 error",
    version="1.0.0",
)

# ==== CORS ====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Debug startup ====
@app.on_event("startup")
async def startup_event():
    print("🚀 DEBUG: Application starting...")
    print(f"🔍 DEBUG: PORT = {os.getenv('PORT', 'NOT_SET')}")
    print(f"🔍 DEBUG: DATABASE_URL = {'SET' if os.getenv('DATABASE_URL') else 'NOT_SET'}")
    print(f"🔍 DEBUG: RAILWAY_ENVIRONMENT = {os.getenv('RAILWAY_ENVIRONMENT', 'NOT_SET')}")
    print("✅ DEBUG: Startup completed successfully!")


# ==== Root endpoint ====
@app.get("/")
def root():
    return {
        "ok": True, 
        "message": "DEBUG: IAM System API is running", 
        "docs": "/docs", 
        "health": "/health",
        "debug": "/debug"
    }

# ==== Health check ====
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "DEBUG: Backend is running"}

# ==== Debug endpoint ====
@app.get("/debug")
def debug_info():
    return {
        "status": "debug",
        "port": os.getenv("PORT", "NOT_SET"),
        "database_url_set": bool(os.getenv("DATABASE_URL")),
        "railway_environment": os.getenv("RAILWAY_ENVIRONMENT", "NOT_SET"),
        "all_env_vars": dict(os.environ)
    }


# ==== Routers ====
# Tạm thời comment out để test
# app.include_router(auth.router)
# app.include_router(user_router.router)
# app.include_router(feature.router)
# app.include_router(rbac.router)
# app.include_router(abac.router)