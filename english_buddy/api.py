from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .llm import create_client, query
from .models import BuddyResponse

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = create_client()
    yield


app = FastAPI(title="English Buddy", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    scene: str


@app.post("/api/query", response_model=BuddyResponse)
async def api_query(req: QueryRequest):
    return query(req.scene, app.state.client)


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


def main():
    import uvicorn

    uvicorn.run("english_buddy.api:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
