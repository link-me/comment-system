from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr
from uuid import uuid4
from pathlib import Path
import json
import datetime

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "comments.json"

def ensure_store():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({"comments": []}, indent=2), encoding="utf-8")

def load():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

class CommentCreate(BaseModel):
    postId: constr(min_length=1)
    author: constr(min_length=1)
    text: constr(min_length=3, max_length=2000)

app = FastAPI(title="comment-system")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ensure_store()

@app.get("/health")
async def health():
    return {"status": "ok", "service": "comment-system"}

@app.get("/comments")
async def list_comments(postId: str | None = None, author: str | None = None):
    db = load()
    items = db.get("comments", [])
    if postId:
        items = [c for c in items if c.get("postId") == postId]
    if author:
        items = [c for c in items if c.get("author") == author]
    return {"count": len(items), "items": items}

@app.post("/comments")
async def create_comment(payload: CommentCreate):
    db = load()
    now = datetime.datetime.utcnow().isoformat()
    comment = {
        "id": str(uuid4()),
        "postId": payload.postId,
        "author": payload.author,
        "text": payload.text,
        "createdAt": now,
        "flagged": False,
    }
    db["comments"].append(comment)
    save(db)
    return comment

@app.delete("/comments/{comment_id}")
async def delete_comment(comment_id: str):
    db = load()
    items = db.get("comments", [])
    idx = next((i for i, c in enumerate(items) if c.get("id") == comment_id), -1)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Not found")
    items.pop(idx)
    db["comments"] = items
    save(db)
    return {"ok": True}

@app.post("/comments/{comment_id}/flag")
async def flag_comment(comment_id: str):
    db = load()
    items = db.get("comments", [])
    for c in items:
        if c.get("id") == comment_id:
            c["flagged"] = True
            save(db)
            return {"id": comment_id, "flagged": True}
    raise HTTPException(status_code=404, detail="Not found")