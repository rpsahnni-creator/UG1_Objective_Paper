"""
One-time migration: fix duplicate 'id' values in the mcqs collection.

Root cause: an earlier seeding run (seed_mcqs.py, executed across multiple
batches) assigned ids using a counter that reset on each run, producing
colliding id strings (e.g. multiple distinct unit2/unit3 questions sharing
the same id) with conflicting answer_index values. This corrupted
/api/quiz/submit scoring (dict keyed by id silently overwrote the correct
answer with whichever duplicate doc was read last).

This script reassigns a guaranteed-unique id per chapter to every existing
document (content, question count, and chapters are preserved — only the
id field is rewritten), based on each document's stable _id ordering.
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]


async def main():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    chapter_ids = await db.mcqs.distinct("chapter_id")
    total_fixed = 0
    for cid in chapter_ids:
        cursor = db.mcqs.find({"chapter_id": cid}, {"_id": 1}).sort("_id", 1)
        docs = await cursor.to_list(length=100000)
        for idx, d in enumerate(docs):
            new_id = f"{cid}-{idx + 1:04d}"
            await db.mcqs.update_one({"_id": d["_id"]}, {"$set": {"id": new_id}})
            total_fixed += 1
        print(f"{cid}: reassigned {len(docs)} unique ids")

    # verification
    for cid in chapter_ids:
        total = await db.mcqs.count_documents({"chapter_id": cid})
        unique_ids = await db.mcqs.distinct("id", {"chapter_id": cid})
        print(f"VERIFY {cid}: total={total} unique_ids={len(unique_ids)} OK={total == len(unique_ids)}")

    print(f"Done. Total docs updated: {total_fixed}")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
