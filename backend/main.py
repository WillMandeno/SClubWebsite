from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="SClub Calendar API",
    description="API for managing college calendar events",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vue dev servers
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

# TODO: Add routes for events, users, authentication

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
