from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .llm import create_client, query
from .models import BuddyResponse
from .store import ResultStatus, store
from .wechat import router as wechat_router

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

app.include_router(wechat_router)


class QueryRequest(BaseModel):
    scene: str


@app.post("/api/query", response_model=BuddyResponse)
async def api_query(req: QueryRequest):
    return query(req.scene, app.state.client)


@app.get("/api/result/{result_id}")
async def get_result(result_id: str):
    entry = store.get(result_id)
    if not entry:
        raise HTTPException(404, "Result not found")
    if entry.status == ResultStatus.PENDING:
        return {"status": "pending", "scene": entry.scene}
    if entry.status == ResultStatus.ERROR:
        return {"status": "error", "error": entry.error}
    return {"status": "done", "result": entry.result.model_dump(), "scene": entry.scene}


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/result/{result_id}")
async def result_page(result_id: str):
    return FileResponse(STATIC_DIR / "result.html")


def main():
    import uvicorn

    uvicorn.run("english_buddy.api:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
