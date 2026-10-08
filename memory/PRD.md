# Introduction to Computer & IT – PRD

## What is this
A bilingual (English + Hindi) mobile app for the FYUGP Semester-I SEC paper
"Introduction to Computer & IT" (3 units, per attached syllabus).

## Users
- Students: free access via "Student Access" (guest login).
- Admin: `kijitechnology@gmail.com` / `admin@123` (free access, admin badge).

## Content
- 3 chapters: Introduction to Computers; Hardware/Software/Office; Networking/Internet.
- Each chapter has:
  - Bilingual study material (6 sections per chapter) in English + Hindi (Devanagari).
  - A bilingual MCQ bank (currently **653 MCQs** total, exceeding the 500 target).

## Screens (expo-router)
1. `/` Welcome — bilingual title, Student + Admin buttons, A/अ toggle.
2. `/admin-login` — simple email/password form with inline error.
3. `/dashboard` — stats, 3 chapter cards, admin badge if applicable.
4. `/chapter/[id]` — segmented tabs: Study Material (with per-section bookmark toggle,
   deep-link `?section=N` auto-scrolls to that section) / MCQ Quiz.
5. `/quiz/[id]` — progress bar, question card, option tiles (reveal correct answer + bilingual explanation).
   `id === "daily"` fetches the mixed Daily Practice set instead of a chapter's MCQs.
6. `/quiz-result` — score %, correct/wrong breakdown, back to chapters. Shows "Daily Practice Result"
   title when the quiz was the daily mixed set.
7. `/bookmarks` — list of all bookmarked study-material sections (per logged-in user), tap to jump
   back into the chapter at that section, swipe/trash icon to remove.

## Backend (FastAPI + Mongo)
- `/api/` health
- `/api/auth/login` (admin), `/api/auth/guest`, `/api/auth/me`
- `/api/chapters`
- `/api/chapters/{id}/study-material`
- `/api/chapters/{id}/mcqs?limit=`
- `/api/quiz/submit`
- `/api/progress` — per-user, per-chapter attempts/best_percent/last_percent (powers dashboard progress rings)
- `/api/bookmarks` (POST add/list GET, DELETE `{chapter_id}/{section_index}`) — per-user saved study sections
- `/api/daily-practice` (GET, no auth) — 10 mixed MCQs (4 unit1 + 3 unit2 + 3 unit3), deterministic per
  calendar date (same set for all users/students that day)
- `/api/daily-practice/status` (GET, auth) — whether the logged-in user completed today's set + score
- MCQs & study material seeded on startup; LLM top-up via `seed_more.py`.

## Feature additions (this session)
- **Chapter Progress Ring**: SVG ring (`react-native-svg`, `src/components/ProgressRing.tsx`) on each
  dashboard chapter card showing best score %, with "Not started" / "Best X%" caption.
- **Bookmark Topics**: bookmark icon on every study-material section heading; `/bookmarks` screen to
  review and jump back to saved topics (auto-scroll).
- **Daily Practice**: dashboard card with a 10-question mixed daily quiz (reuses existing quiz engine
  via `id === "daily"`), "Completed Today • X%" badge once done for the day.
- **Data-integrity fix**: migrated 653 existing MCQ docs to guarantee unique `id` per chapter
  (`fix_duplicate_mcq_ids.py`, one-time, already run) — unit2/unit3 previously had duplicate ids from
  historical multi-batch seeding, which silently corrupted `/api/quiz/submit` scoring. Startup seeding
  logic also hardened (per-chapter id counters) to prevent recurrence.

## Design
Editorial palette (terracotta `#8C3B32` + paper `#FDFBF7`), generous spacing,
serif-weight headings, no gradient/purple AI slop. Hindi/English toggle (`A / अ`)
on every screen (top-right).
