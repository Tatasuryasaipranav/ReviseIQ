"""
main.py — ExamCoach Application Entry Point
Run: python main.py  →  open http://localhost:8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from pathlib import Path
import uvicorn
from database import init_db
from routes.api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("\n" + "="*50)
    print("  🎓 ExamCoach is RUNNING!")
    print("  🌐 Open: http://localhost:8000")
    print("  📖 API:  http://localhost:8000/docs")
    print("="*50 + "\n")
    yield

app = FastAPI(title="ExamCoach API", version="2.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_origin_regex=".*",
    allow_credentials=False, allow_methods=["*"],
    allow_headers=["*"], expose_headers=["*"])

app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def frontend():
    p = Path(__file__).parent / "index.html"
    if p.exists():
        return HTMLResponse(p.read_text("utf-8"))
    return HTMLResponse("<h1>Put index.html here</h1>")

@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_excludes=["*.db"])
