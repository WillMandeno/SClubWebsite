from fastapi import FastAPI, Response
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
from sqlalchemy import create_engine, text
from backend.database import DATABASE_URL

# Create the FastAPI app
app = FastAPI(title="SClub Calendar API")

# Add CORS (Cross Origin Resource Sharing) middleware so the Vite dev server can call the API
app.add_middleware(
    CORSMiddleware,
    # For development: explicitly whitelist the Vite dev server origins
    allow_origins=[
        # Production frontend URL
        "https://sclub-calendar.vercel.app",
        # Development frontend URLs 
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
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

@app.head("/health")
async def health_check_head():
    return Response(status_code=200)


app.include_router(auth_router)
app.include_router(events_router)
app.include_router(admin_router)

@app.middleware("http")
async def log_request(request, call_next):
    # Only inspect bodies for methods that may include one.
    if request.method in ("POST", "PUT", "PATCH"):
        # Read the body (consumes the incoming stream) and log a safe preview.
        body = await request.body()
        preview = body.decode(errors="replace")[:8192]
        print("RAW BODY:", preview)

        # Make the body available again to downstream handlers by
        # replacing the request's receive callable with one that returns
        # the same body payload.
        async def _receive() -> dict:
            return {"type": "http.request", "body": body, "more_body": False}

        request._receive = _receive

    response = await call_next(request)
    return response

if __name__ == "__main__":
    # Run with the venv's python to ensure correct packages are used
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
