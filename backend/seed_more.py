"""Top-up MCQs to ~500 using LLM, idempotent (skips if already enough)."""
import asyncio, json, os, re, sys, time
from pathlib import Path
from dotenv import load_dotenv
sys.path.insert(0, str(Path(__file__).parent))
load_dotenv(Path(__file__).parent / ".env")
from emergentintegrations.llm.chat import LlmChat, UserMessage  # noqa
from motor.motor_asyncio import AsyncIOMotorClient

API_KEY = os.environ["EMERGENT_LLM_KEY"]
client = AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client[os.environ["DB_NAME"]]

CHAPTERS = [
    {"id":"unit1","name_en":"UNIT-I Introduction to Computers",
     "topics":["Characteristics of computers","Block diagram & CPU (CU, ALU)","Hardware vs software","Types & purposes of computers","Generations 1-5","Number systems and conversions"],
     "target": 170},
    {"id":"unit2","name_en":"UNIT-II Hardware, Software & Office Apps",
     "topics":["Input / output devices","Primary and secondary storage","Memory hierarchy, RAM / ROM types","System vs application software","Operating systems","MS Word features","MS Excel formulas","MS PowerPoint features"],
     "target": 170},
    {"id":"unit3","name_en":"UNIT-III Networking & Internet",
     "topics":["Computer networks need and definition","LAN / MAN / WAN / PAN","Network devices modem router switch hub","IP addressing and DNS","HTTP, email protocols","Web browsing and search engines","AI, Big Data, Blockchain"],
     "target": 160},
]

SYS = ("You write exam-style MCQs for Indian B.Sc semester-1 students "
       "(course: Introduction to Computer & IT). Return ONLY a valid JSON array. "
       "Each question must have faithful Hindi (Devanagari) translation of question, "
       "4 options, and explanation. Vary difficulty.")

PROMPT = """Give {n} new MCQs on "{topic}" for chapter "{ch}". Avoid duplicates.
Schema:
[{{"question_en":"","question_hi":"","options_en":["","","",""],"options_hi":["","","",""],"answer_index":0,"explanation_en":"","explanation_hi":"","difficulty":"easy|medium|hard"}}]
JSON array only.
"""

def extract(text):
    text = re.sub(r"^```(?:json)?","",text.strip()).strip()
    text = re.sub(r"```$","",text).strip()
    dec = json.JSONDecoder(); i = 0; out = []
    while i < len(text):
        while i < len(text) and text[i] != "[": i += 1
        if i >= len(text): break
        try:
            obj, end = dec.raw_decode(text, i)
        except Exception: break
        if isinstance(obj, list): out.extend(obj)
        i = end
    return out

async def gen(ch, topic, n, idx):
    chat = LlmChat(api_key=API_KEY, session_id=f"topup-{ch['id']}-{idx}", system_message=SYS).with_model("gemini","gemini-3-flash-preview")
    full = ""
    async for ev in chat.stream_message(UserMessage(text=PROMPT.format(n=n, topic=topic, ch=ch["name_en"]))):
        if hasattr(ev, "content"): full += ev.content
    try: data = extract(full)
    except Exception as e:
        print("  parse err", e); return []
    good = []
    for q in data:
        if (isinstance(q.get("options_en"),list) and len(q["options_en"])==4
            and isinstance(q.get("options_hi"),list) and len(q["options_hi"])==4
            and isinstance(q.get("answer_index"),int) and 0<=q["answer_index"]<=3
            and q.get("question_en") and q.get("question_hi")):
            q["chapter_id"] = ch["id"]
            good.append(q)
    return good

async def main():
    all_new = []
    for ch in CHAPTERS:
        have = await db.mcqs.count_documents({"chapter_id": ch["id"]})
        need = max(0, ch["target"] - have)
        print(f"{ch['id']}: have {have}, need {need}")
        if need == 0: continue
        batch = 10; i = 0; got = 0
        while got < need and i < 30:
            topic = ch["topics"][i % len(ch["topics"])]
            n = min(batch, need - got)
            t0 = time.time()
            try: res = await gen(ch, topic, n, i)
            except Exception as e: print("  err", e); res = []
            print(f"  batch {i+1} topic='{topic[:40]}' n={n} -> {len(res)} ({time.time()-t0:.1f}s)")
            if res:
                base = have + got
                for j, r in enumerate(res):
                    r["id"] = f"{ch['id']}-{(base+j+1):04d}"
                await db.mcqs.insert_many(res)
                all_new.extend(res)
                got += len(res)
            i += 1
    print(f"Added {len(all_new)} new MCQs")

asyncio.run(main())
