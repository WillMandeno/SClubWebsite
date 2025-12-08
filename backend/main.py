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

# Create the FastAPI app
app = FastAPI(title="SClub Calendar API")

# Add CORS middleware so the Vite dev server can call the API
app.add_middleware(
    CORSMiddleware,
    # For development: explicitly whitelist the Vite dev server origins
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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


if __name__ == "__main__":
    # Run with the venv's python to ensure correct packages are used
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
