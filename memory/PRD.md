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
4. `/chapter/[id]` — segmented tabs: Study Material / MCQ Quiz.
5. `/quiz/[id]` — progress bar, question card, option tiles (reveal correct answer + bilingual explanation).
6. `/quiz-result` — score %, correct/wrong breakdown, back to chapters.

## Backend (FastAPI + Mongo)
- `/api/` health
- `/api/auth/login` (admin), `/api/auth/guest`, `/api/auth/me`
- `/api/chapters`
- `/api/chapters/{id}/study-material`
- `/api/chapters/{id}/mcqs?limit=`
- `/api/quiz/submit`
- MCQs & study material seeded on startup; LLM top-up via `seed_more.py`.

## Design
Editorial palette (terracotta `#8C3B32` + paper `#FDFBF7`), generous spacing,
serif-weight headings, no gradient/purple AI slop. Hindi/English toggle (`A / अ`)
on every screen (top-right).
