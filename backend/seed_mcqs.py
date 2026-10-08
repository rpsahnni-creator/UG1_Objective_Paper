"""
Seed MCQ bank. Generates ~500 bilingual MCQs chapter-wise using
Gemini via emergentintegrations and writes to content/mcqs.json.

Run once:  cd /app/backend && python seed_mcqs.py
"""
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from emergentintegrations.llm.chat import LlmChat, UserMessage  # noqa: E402

API_KEY = os.environ["EMERGENT_LLM_KEY"]
OUT = Path(__file__).parent / "content" / "mcqs.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

CHAPTERS = [
    {
        "id": "unit1",
        "name_en": "UNIT-I: Introduction to Computers",
        "topics": [
            "Computer system characteristics and capabilities",
            "Hardware vs Software, Block diagram of a computer",
            "Types, purpose and components of computers",
            "Generations of computers (1st to 5th)",
            "Functional unit: Input, CPU (CU, ALU), Output, Storage",
            "Number systems: Binary, Decimal, Octal, Hexadecimal and conversions",
        ],
        "target": 170,
    },
    {
        "id": "unit2",
        "name_en": "UNIT-II: Computer Hardware, Software & Office Applications",
        "topics": [
            "Basics of input/output devices (keyboard, mouse, scanner, monitor, printer)",
            "Storage: primary (RAM/ROM) and secondary (HDD, SSD, Optical, USB)",
            "Memory types and hierarchy",
            "System software vs Application software",
            "Overview of operating systems (Windows, Linux)",
            "MS Word for document editing",
            "MS Excel for data handling (formulas, cells, charts)",
            "MS PowerPoint for presentations",
        ],
        "target": 170,
    },
    {
        "id": "unit3",
        "name_en": "UNIT-III: Networking and Internet",
        "topics": [
            "Computer Network: definition and need",
            "Types of networks: LAN, MAN, WAN",
            "Network devices: modem, router, switch, hub",
            "IP addressing and DNS",
            "HTTP, Email, Web browsing and search engines",
            "Emerging Technologies: AI, Big Data, Blockchain",
        ],
        "target": 160,
    },
]

SYSTEM = (
    "You are an expert computer science teacher writing multiple-choice questions "
    "for Indian undergraduate students (FYUGP Semester-I, 'Introduction to Computer & IT'). "
    "Write questions that are factually accurate, exam-style, varied in difficulty "
    "(easy, medium, hard), and cover concepts, not trivia. Each question MUST include a "
    "clear English version AND a faithful Hindi (Devanagari) translation of the "
    "question, the 4 options, and a 1-2 sentence explanation. "
    "Return ONLY a valid JSON array. No prose, no code fences."
)

PROMPT_TEMPLATE = """Generate {n} multiple-choice questions on the topic: "{topic}"
for the chapter "{chapter}".

STRICT JSON SCHEMA (array of objects):
[
  {{
    "question_en": "string",
    "question_hi": "string (Devanagari)",
    "options_en": ["A", "B", "C", "D"],
    "options_hi": ["A in Hindi", "B in Hindi", "C in Hindi", "D in Hindi"],
    "answer_index": 0,            // integer 0..3
    "explanation_en": "string",
    "explanation_hi": "string (Devanagari)",
    "difficulty": "easy|medium|hard"
  }}
]

Rules:
- Exactly 4 options.
- answer_index is 0-based.
- Keep options concise (<= 10 words each).
- Make distractors plausible.
- Avoid duplicates with earlier batches.
- Return ONLY the JSON array, nothing else.
"""


def extract_json_array(text: str):
    # Strip code fences if any
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    # Model can emit multiple JSON arrays back-to-back. Decode each with
    # raw_decode and merge.
    decoder = json.JSONDecoder()
    i = 0
    merged = []
    while i < len(text):
        # advance to next '['
        while i < len(text) and text[i] != "[":
            i += 1
        if i >= len(text):
            break
        try:
            obj, end = decoder.raw_decode(text, i)
        except json.JSONDecodeError:
            break
        if isinstance(obj, list):
            merged.extend(obj)
        i = end
    if not merged:
        raise ValueError("no JSON array found")
    return merged


async def generate_batch(chapter, topic, n, batch_idx):
    chat = LlmChat(
        api_key=API_KEY,
        session_id=f"mcq-{chapter['id']}-{batch_idx}",
        system_message=SYSTEM,
    ).with_model("gemini", "gemini-3-flash-preview")
    msg = UserMessage(
        text=PROMPT_TEMPLATE.format(n=n, topic=topic, chapter=chapter["name_en"])
    )
    # Collect streamed text
    full = ""
    async for ev in chat.stream_message(msg):
        if hasattr(ev, "content"):
            full += ev.content
    try:
        data = extract_json_array(full)
    except Exception as e:
        print(f"   parse error ({e}); raw head: {full[:200]!r}")
        return []
    cleaned = []
    for q in data:
        if (
            isinstance(q.get("options_en"), list)
            and len(q["options_en"]) == 4
            and isinstance(q.get("options_hi"), list)
            and len(q["options_hi"]) == 4
            and isinstance(q.get("answer_index"), int)
            and 0 <= q["answer_index"] <= 3
            and q.get("question_en")
            and q.get("question_hi")
        ):
            q["chapter_id"] = chapter["id"]
            q["topic"] = topic
            cleaned.append(q)
    return cleaned


async def main():
    all_q = []
    batch_size = 10
    for chapter in CHAPTERS:
        print(f"\n== {chapter['name_en']} — target {chapter['target']} ==")
        collected = 0
        topic_idx = 0
        batch_idx = 0
        while collected < chapter["target"]:
            topic = chapter["topics"][topic_idx % len(chapter["topics"])]
            needed = min(batch_size, chapter["target"] - collected)
            print(f"  batch {batch_idx+1}: topic '{topic[:50]}' n={needed}")
            t0 = time.time()
            try:
                batch = await generate_batch(chapter, topic, needed, batch_idx)
            except Exception as e:
                print(f"   LLM error: {e}; retrying once")
                try:
                    batch = await generate_batch(chapter, topic, needed, batch_idx)
                except Exception as e2:
                    print(f"   second LLM error: {e2}; skip")
                    batch = []
            print(
                f"   got {len(batch)} in {time.time()-t0:.1f}s — chapter total {collected+len(batch)}"
            )
            all_q.extend(batch)
            collected += len(batch)
            topic_idx += 1
            batch_idx += 1
            if batch_idx > chapter["target"] // 2 + 10:
                break  # safety
        print(f"  final for {chapter['id']}: {collected}")
    OUT.write_text(json.dumps(all_q, ensure_ascii=False, indent=2))
    print(f"\nTotal {len(all_q)} MCQs saved to {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
