from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Optional: ensure repo root is on sys.path when running from inside the
# `backend/` folder. Prefer running uvicorn in package mode from the repo
# root (python -m uvicorn backend.main:app) so package imports work.
_this_dir = os.path.dirname(os.path.abspath(__file__))
_proj_root = os.path.dirname(_this_dir)
if _proj_root not in sys.path:
    sys.path.insert(0, _proj_root)

from backend.auth import router as auth_router
from backend.events import router as events_router
from backend.admin import router as admin_router
from fastapi import Header, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy import create_engine, text
from backend.database import DATABASE_URL

# Create the FastAPI app
app = FastAPI(title="SClub Calendar API")

# Add CORS (Cross Origin Resource Sharing) middleware so the Vite dev server can call the API
app.add_middleware(
    CORSMiddleware,
    # For development: explicitly whitelist the Vite dev server origins
    allow_origins=["http://localhost:5173", "https://sclub-calendar.vercel.app"],
    # Keep credentials allowed if you plan to use cookies or other credentialed requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "SClub Calendar API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(auth_router)
app.include_router(events_router)
app.include_router(admin_router)


@app.get("/internal/test-db")
async def internal_test_db(x_admin_password: str | None = Header(None)):
    """Temporary endpoint to test DB connectivity from the running service.

    Protects itself by requiring the `X-Admin-Password` header to match the
    `ADMIN_PASSWORD` environment variable. Returns `SELECT 1` result or a
    plain-text error for debugging.
    """
    secret = os.getenv("ADMIN_PASSWORD")
    if not secret or x_admin_password != secret:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        engine = create_engine(
            DATABASE_URL,
            connect_args={"sslmode": "require"},
            pool_pre_ping=True,
            pool_size=1,
            max_overflow=0,
            pool_timeout=10,
        )
        with engine.connect() as conn:
            r = conn.execute(text("SELECT 1")).scalar()
        return {"ok": True, "result": r}
    except Exception as e:
        return PlainTextResponse(str(e), status_code=500)


if __name__ == "__main__":
    # Run with the venv's python to ensure correct packages are used
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
