from fastapi import FastAPI
from app.routes import analyze
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ FIXED PATH
frontend_path = os.path.join(BASE_DIR, "app", "frontend")

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))
