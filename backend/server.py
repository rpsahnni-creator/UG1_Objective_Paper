from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import sys
import logging
import jwt
import uuid
import random
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")
sys.path.insert(0, str(ROOT_DIR))

from content.study_material import STUDY_MATERIAL  # noqa: E402
from content.mcq_bank import MCQS  # noqa: E402

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]
ADMIN_EMAIL = os.environ["ADMIN_EMAIL"].lower()
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = "HS256"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

app = FastAPI(title="Introduction to Computer & IT")
api = APIRouter(prefix="/api")
bearer = HTTPBearer(auto_error=False)


# -------- Models --------
class Chapter(BaseModel):
    id: str
    name_en: str
    name_hi: str
    icon: str
    description_en: str
    description_hi: str
    question_count: int


class Section(BaseModel):
    heading_en: str
    heading_hi: str
    body_en: str
    body_hi: str


class StudyMaterialOut(BaseModel):
    chapter_id: str
    title_en: str
    title_hi: str
    sections: List[Section]


class MCQOut(BaseModel):
    id: str
    chapter_id: str
    question_en: str
    question_hi: str
    options_en: List[str]
    options_hi: List[str]
    answer_index: int
    explanation_en: str
    explanation_hi: str
    difficulty: str


class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    token: str
    is_admin: bool
    email: str


class SubmitAnswer(BaseModel):
    question_id: str
    selected: int


class QuizSubmit(BaseModel):
    chapter_id: str
    answers: List[SubmitAnswer]


class QuizResult(BaseModel):
    chapter_id: str
    total: int
    correct: int
    wrong: int
    percent: float
    taken_at: datetime


class ProgressOut(BaseModel):
    chapter_id: str
    attempts: int
    best_percent: float
    last_percent: float
    last_taken_at: Optional[datetime] = None


class BookmarkIn(BaseModel):
    chapter_id: str
    section_index: int
    heading_en: str
    heading_hi: str


class BookmarkOut(BaseModel):
    id: str
    chapter_id: str
    chapter_name_en: str
    chapter_name_hi: str
    section_index: int
    heading_en: str
    heading_hi: str
    created_at: datetime


class DailyPracticeOut(BaseModel):
    date: str
    questions: List[MCQOut]


class DailyStatusOut(BaseModel):
    date: str
    completed: bool
    percent: Optional[float] = None
    correct: Optional[int] = None
    total: Optional[int] = None


# -------- Chapter metadata --------
CHAPTERS_META = {
    "unit1": {
        "name_en": "UNIT-I: Introduction to Computers",
        "name_hi": "इकाई-I: कंप्यूटर का परिचय",
        "icon": "cpu",
        "description_en": "Characteristics, block diagram, generations, functional units and number systems.",
        "description_hi": "विशेषताएँ, ब्लॉक आरेख, पीढ़ियाँ, कार्यात्मक इकाइयाँ और संख्या पद्धतियाँ।",
    },
    "unit2": {
        "name_en": "UNIT-II: Hardware, Software & Office Applications",
        "name_hi": "इकाई-II: हार्डवेयर, सॉफ्टवेयर और ऑफ़िस अनुप्रयोग",
        "icon": "hard-drive",
        "description_en": "I/O devices, storage, memory types, operating systems, MS Word, Excel, PowerPoint.",
        "description_hi": "I/O उपकरण, भंडारण, मेमोरी, ऑपरेटिंग सिस्टम, MS Word, Excel, PowerPoint।",
    },
    "unit3": {
        "name_en": "UNIT-III: Networking and Internet",
        "name_hi": "इकाई-III: नेटवर्किंग और इंटरनेट",
        "icon": "wifi",
        "description_en": "LAN/MAN/WAN, network devices, IP/DNS, HTTP, Email, AI, Big Data, Blockchain.",
        "description_hi": "LAN/MAN/WAN, नेटवर्क उपकरण, IP/DNS, HTTP, ईमेल, AI, बिग डेटा, ब्लॉकचेन।",
    },
}


# -------- Startup: seed MCQs & study material --------
@app.on_event("startup")
async def startup():
    # Study material (idempotent upsert)
    for mat in STUDY_MATERIAL:
        await db.study_material.update_one(
            {"chapter_id": mat["chapter_id"]}, {"$set": mat}, upsert=True
        )
    # MCQs: seed only once (keep stable ids via a PER-CHAPTER counter so ids
    # never collide across chapters even if the content list order changes)
    if await db.mcqs.count_documents({}) == 0:
        docs = []
        counters: dict = {}
        for q in MCQS:
            cid = q["chapter_id"]
            counters[cid] = counters.get(cid, 0) + 1
            d = dict(q)
            d["id"] = f"{cid}-{counters[cid]:04d}"
            docs.append(d)
        if docs:
            await db.mcqs.insert_many(docs)
        logging.info(f"Seeded {len(docs)} MCQs")


# -------- Auth helpers --------
def make_token(email: str, is_admin: bool) -> str:
    payload = {
        "email": email,
        "is_admin": is_admin,
        "exp": datetime.now(timezone.utc) + timedelta(days=30),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    return decode_token(authorization.split(" ", 1)[1])


# -------- Routes --------
@api.get("/")
async def root():
    return {"service": "intro-computer-it", "status": "ok"}


@api.post("/auth/login", response_model=LoginOut)
async def login(body: LoginIn):
    uname = body.username.strip().lower()
    if uname == ADMIN_EMAIL and body.password == ADMIN_PASSWORD:
        token = make_token(uname, True)
        return LoginOut(token=token, is_admin=True, email=uname)
    raise HTTPException(status_code=401, detail="Invalid credentials")


@api.post("/auth/guest", response_model=LoginOut)
async def guest():
    """Free student access — no password required."""
    gid = f"guest-{uuid.uuid4().hex[:8]}@local"
    token = make_token(gid, False)
    return LoginOut(token=token, is_admin=False, email=gid)


@api.get("/auth/me")
async def me(user: dict = Depends(current_user)):
    return {"email": user["email"], "is_admin": user.get("is_admin", False)}


@api.get("/chapters", response_model=List[Chapter])
async def list_chapters():
    out = []
    for cid, meta in CHAPTERS_META.items():
        qc = await db.mcqs.count_documents({"chapter_id": cid})
        out.append(Chapter(id=cid, question_count=qc, **meta))
    return out


@api.get("/chapters/{chapter_id}/study-material", response_model=StudyMaterialOut)
async def get_study_material(chapter_id: str):
    doc = await db.study_material.find_one({"chapter_id": chapter_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return StudyMaterialOut(**doc)


@api.get("/chapters/{chapter_id}/mcqs", response_model=List[MCQOut])
async def get_mcqs(chapter_id: str, limit: int = 50):
    cursor = db.mcqs.find({"chapter_id": chapter_id}, {"_id": 0}).limit(limit)
    docs = await cursor.to_list(length=limit)
    return [MCQOut(**d) for d in docs]


@api.post("/quiz/submit")
async def submit_quiz(body: QuizSubmit, user: dict = Depends(current_user)):
    qids = [a.question_id for a in body.answers]
    docs = await db.mcqs.find({"id": {"$in": qids}}, {"_id": 0}).to_list(length=len(qids))
    answer_map = {d["id"]: d["answer_index"] for d in docs}
    correct = 0
    details = []
    for a in body.answers:
        is_right = answer_map.get(a.question_id) == a.selected
        if is_right:
            correct += 1
        details.append({
            "question_id": a.question_id,
            "selected": a.selected,
            "correct_index": answer_map.get(a.question_id),
            "is_correct": is_right,
        })
    total = len(body.answers)
    wrong = total - correct
    pct = (correct / total * 100) if total else 0.0
    result = {
        "id": str(uuid.uuid4()),
        "email": user["email"],
        "chapter_id": body.chapter_id,
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "percent": pct,
        "taken_at": datetime.now(timezone.utc),
        "details": details,
    }
    await db.quiz_results.insert_one(dict(result))
    result.pop("_id", None)
    return result


# -------- Progress --------
@api.get("/progress", response_model=List[ProgressOut])
async def get_progress(user: dict = Depends(current_user)):
    docs = await db.quiz_results.find(
        {"email": user["email"], "chapter_id": {"$in": list(CHAPTERS_META.keys())}},
        {"_id": 0, "chapter_id": 1, "percent": 1, "taken_at": 1},
    ).sort("taken_at", 1).to_list(length=10000)
    agg: dict = {}
    for d in docs:
        cid = d["chapter_id"]
        cur = agg.setdefault(cid, {"attempts": 0, "best_percent": 0.0, "last_percent": 0.0, "last_taken_at": None})
        cur["attempts"] += 1
        cur["best_percent"] = max(cur["best_percent"], d["percent"])
        cur["last_percent"] = d["percent"]
        cur["last_taken_at"] = d["taken_at"]
    return [ProgressOut(chapter_id=cid, **vals) for cid, vals in agg.items()]


# -------- Bookmarks --------
@api.post("/bookmarks", response_model=BookmarkOut)
async def add_bookmark(body: BookmarkIn, user: dict = Depends(current_user)):
    meta = CHAPTERS_META.get(body.chapter_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Chapter not found")
    existing = await db.bookmarks.find_one({
        "email": user["email"], "chapter_id": body.chapter_id, "section_index": body.section_index,
    })
    if existing:
        return BookmarkOut(
            id=existing["id"], chapter_id=existing["chapter_id"],
            chapter_name_en=meta["name_en"], chapter_name_hi=meta["name_hi"],
            section_index=existing["section_index"], heading_en=existing["heading_en"],
            heading_hi=existing["heading_hi"], created_at=existing["created_at"],
        )
    doc = {
        "id": str(uuid.uuid4()),
        "email": user["email"],
        "chapter_id": body.chapter_id,
        "section_index": body.section_index,
        "heading_en": body.heading_en,
        "heading_hi": body.heading_hi,
        "created_at": datetime.now(timezone.utc),
    }
    await db.bookmarks.insert_one(dict(doc))
    return BookmarkOut(
        id=doc["id"], chapter_id=doc["chapter_id"],
        chapter_name_en=meta["name_en"], chapter_name_hi=meta["name_hi"],
        section_index=doc["section_index"], heading_en=doc["heading_en"],
        heading_hi=doc["heading_hi"], created_at=doc["created_at"],
    )


@api.get("/bookmarks", response_model=List[BookmarkOut])
async def list_bookmarks(user: dict = Depends(current_user)):
    docs = await db.bookmarks.find({"email": user["email"]}, {"_id": 0}).sort("created_at", -1).to_list(length=1000)
    out = []
    for d in docs:
        meta = CHAPTERS_META.get(d["chapter_id"], {})
        out.append(BookmarkOut(
            id=d["id"], chapter_id=d["chapter_id"],
            chapter_name_en=meta.get("name_en", d["chapter_id"]),
            chapter_name_hi=meta.get("name_hi", d["chapter_id"]),
            section_index=d["section_index"], heading_en=d["heading_en"], heading_hi=d["heading_hi"],
            created_at=d["created_at"],
        ))
    return out


@api.delete("/bookmarks/{chapter_id}/{section_index}")
async def delete_bookmark(chapter_id: str, section_index: int, user: dict = Depends(current_user)):
    await db.bookmarks.delete_one(
        {"email": user["email"], "chapter_id": chapter_id, "section_index": section_index}
    )
    return {"ok": True}


# -------- Daily Practice --------
def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


async def _build_daily_questions(date_str: str):
    rng = random.Random(date_str)
    chapter_ids = list(CHAPTERS_META.keys())
    splits = [4, 3, 3]
    selected = []
    for cid, n in zip(chapter_ids, splits):
        docs = await db.mcqs.find({"chapter_id": cid}, {"_id": 0}).to_list(length=10000)
        if not docs:
            continue
        k = min(n, len(docs))
        selected.extend(rng.sample(docs, k))
    rng.shuffle(selected)
    return selected


@api.get("/daily-practice", response_model=DailyPracticeOut)
async def daily_practice():
    date_str = _today_str()
    questions = await _build_daily_questions(date_str)
    return DailyPracticeOut(date=date_str, questions=[MCQOut(**q) for q in questions])


@api.get("/daily-practice/status", response_model=DailyStatusOut)
async def daily_practice_status(user: dict = Depends(current_user)):
    date_str = _today_str()
    start = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    doc = await db.quiz_results.find(
        {"email": user["email"], "chapter_id": "daily", "taken_at": {"$gte": start, "$lt": end}},
    ).sort("taken_at", -1).to_list(length=1)
    if not doc:
        return DailyStatusOut(date=date_str, completed=False)
    d = doc[0]
    return DailyStatusOut(date=date_str, completed=True, percent=d["percent"], correct=d["correct"], total=d["total"])


app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")


@app.on_event("shutdown")
async def shutdown():
    client.close()
