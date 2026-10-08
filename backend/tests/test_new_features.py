"""
Tests for 3 NEW features: Progress tracking, Bookmarks CRUD, Daily Practice.
Reuses guest auth token for authenticated endpoints.
"""
import os
import pytest
import requests

BASE_URL = os.environ.get("EXPO_BACKEND_URL", "").rstrip("/") or os.environ.get("EXPO_PUBLIC_BACKEND_URL", "").rstrip("/")


@pytest.fixture(scope="module")
def api_client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def guest_token(api_client):
    r = api_client.post(f"{BASE_URL}/api/auth/guest")
    assert r.status_code == 200
    return r.json()["token"]


@pytest.fixture(scope="module")
def auth_headers(guest_token):
    return {"Authorization": f"Bearer {guest_token}"}


class TestProgress:
    def test_progress_requires_auth(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/progress")
        assert r.status_code == 401

    def test_progress_empty_for_new_guest(self, api_client, auth_headers):
        r = api_client.get(f"{BASE_URL}/api/progress", headers=auth_headers)
        assert r.status_code == 200
        assert r.json() == []

    def test_progress_updates_after_quiz_submit(self, api_client, auth_headers):
        # get mcqs for unit1
        mcqs = api_client.get(f"{BASE_URL}/api/chapters/unit1/mcqs?limit=5").json()
        assert len(mcqs) > 0
        answers = [{"question_id": q["id"], "selected": q["answer_index"]} for q in mcqs]
        submit = api_client.post(
            f"{BASE_URL}/api/quiz/submit",
            json={"chapter_id": "unit1", "answers": answers},
            headers=auth_headers,
        )
        assert submit.status_code == 200
        body = submit.json()
        assert body["correct"] == len(mcqs)
        assert body["percent"] == 100.0

        prog = api_client.get(f"{BASE_URL}/api/progress", headers=auth_headers)
        assert prog.status_code == 200
        data = prog.json()
        assert len(data) == 1
        assert data[0]["chapter_id"] == "unit1"
        assert data[0]["attempts"] == 1
        assert data[0]["best_percent"] == 100.0
        assert data[0]["last_percent"] == 100.0
        assert data[0]["last_taken_at"] is not None

    def test_progress_only_includes_chapter_ids(self, api_client, auth_headers):
        prog = api_client.get(f"{BASE_URL}/api/progress", headers=auth_headers)
        for p in prog.json():
            assert p["chapter_id"] in ["unit1", "unit2", "unit3"]


class TestMcqIdIntegrity:
    """Regression tests for duplicate-mcq-id scoring bug (fixed via fix_duplicate_mcq_ids.py).
    Uses its OWN isolated guest token (not the shared module-scoped guest_token) to avoid
    polluting progress state relied upon by TestProgress tests."""

    @pytest.fixture(scope="class")
    def isolated_auth_headers(self):
        s = requests.Session()
        r = s.post(f"{BASE_URL}/api/auth/guest")
        token = r.json()["token"]
        return {"Authorization": f"Bearer {token}"}

    @pytest.mark.parametrize("chapter_id,expected_total", [("unit1", 171), ("unit2", 199), ("unit3", 283)])
    def test_mcq_ids_are_unique_per_chapter(self, api_client, chapter_id, expected_total):
        mcqs = api_client.get(f"{BASE_URL}/api/chapters/{chapter_id}/mcqs?limit=10000").json()
        assert len(mcqs) == expected_total
        ids = [q["id"] for q in mcqs]
        assert len(set(ids)) == expected_total, f"{chapter_id} has duplicate ids: {len(set(ids))} unique of {len(ids)}"

    @pytest.mark.parametrize("chapter_id", ["unit1", "unit2", "unit3"])
    def test_full_chapter_all_correct_scores_100(self, api_client, isolated_auth_headers, chapter_id):
        mcqs = api_client.get(f"{BASE_URL}/api/chapters/{chapter_id}/mcqs?limit=10000").json()
        answers = [{"question_id": q["id"], "selected": q["answer_index"]} for q in mcqs]
        submit = api_client.post(
            f"{BASE_URL}/api/quiz/submit",
            json={"chapter_id": chapter_id, "answers": answers},
            headers=isolated_auth_headers,
        )
        assert submit.status_code == 200
        body = submit.json()
        assert body["correct"] == len(mcqs)
        assert body["total"] == len(mcqs)
        assert body["percent"] == 100.0


class TestBookmarks:
    def test_bookmarks_requires_auth(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/bookmarks")
        assert r.status_code == 401

    def test_add_bookmark_and_verify_persistence(self, api_client, auth_headers):
        payload = {
            "chapter_id": "unit1",
            "section_index": 0,
            "heading_en": "TEST_Section Heading",
            "heading_hi": "TEST_खंड शीर्षक",
        }
        r = api_client.post(f"{BASE_URL}/api/bookmarks", json=payload, headers=auth_headers)
        assert r.status_code == 200
        created = r.json()
        assert created["chapter_id"] == "unit1"
        assert created["section_index"] == 0
        assert created["heading_en"] == "TEST_Section Heading"
        assert "id" in created

        # GET to verify persisted
        lst = api_client.get(f"{BASE_URL}/api/bookmarks", headers=auth_headers)
        assert lst.status_code == 200
        ids = [b["id"] for b in lst.json()]
        assert created["id"] in ids

    def test_add_duplicate_bookmark_is_idempotent(self, api_client, auth_headers):
        payload = {
            "chapter_id": "unit1",
            "section_index": 0,
            "heading_en": "TEST_Section Heading",
            "heading_hi": "TEST_खंड शीर्षक",
        }
        r1 = api_client.post(f"{BASE_URL}/api/bookmarks", json=payload, headers=auth_headers)
        r2 = api_client.post(f"{BASE_URL}/api/bookmarks", json=payload, headers=auth_headers)
        assert r1.json()["id"] == r2.json()["id"]

        lst = api_client.get(f"{BASE_URL}/api/bookmarks", headers=auth_headers)
        matching = [b for b in lst.json() if b["chapter_id"] == "unit1" and b["section_index"] == 0]
        assert len(matching) == 1

    def test_delete_bookmark_and_verify_removed(self, api_client, auth_headers):
        payload = {
            "chapter_id": "unit2",
            "section_index": 1,
            "heading_en": "TEST_Another Section",
            "heading_hi": "TEST_अन्य खंड",
        }
        api_client.post(f"{BASE_URL}/api/bookmarks", json=payload, headers=auth_headers)
        d = api_client.delete(f"{BASE_URL}/api/bookmarks/unit2/1", headers=auth_headers)
        assert d.status_code == 200

        lst = api_client.get(f"{BASE_URL}/api/bookmarks", headers=auth_headers)
        matching = [b for b in lst.json() if b["chapter_id"] == "unit2" and b["section_index"] == 1]
        assert len(matching) == 0

    def test_bookmark_invalid_chapter_404(self, api_client, auth_headers):
        payload = {
            "chapter_id": "unit99",
            "section_index": 0,
            "heading_en": "x",
            "heading_hi": "x",
        }
        r = api_client.post(f"{BASE_URL}/api/bookmarks", json=payload, headers=auth_headers)
        assert r.status_code == 404

    @pytest.fixture(autouse=True, scope="class")
    def cleanup(self, api_client, auth_headers):
        yield
        api_client.delete(f"{BASE_URL}/api/bookmarks/unit1/0", headers=auth_headers)
        api_client.delete(f"{BASE_URL}/api/bookmarks/unit2/1", headers=auth_headers)


class TestDailyPractice:
    def test_daily_practice_no_auth_required(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/daily-practice")
        assert r.status_code == 200
        body = r.json()
        assert "date" in body
        assert len(body["questions"]) == 10

    def test_daily_practice_mix_counts(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/daily-practice")
        qs = r.json()["questions"]
        counts = {}
        for q in qs:
            counts[q["chapter_id"]] = counts.get(q["chapter_id"], 0) + 1
        assert counts.get("unit1", 0) == 4
        assert counts.get("unit2", 0) == 3
        assert counts.get("unit3", 0) == 3

    def test_daily_practice_deterministic_same_day(self, api_client):
        r1 = api_client.get(f"{BASE_URL}/api/daily-practice")
        r2 = api_client.get(f"{BASE_URL}/api/daily-practice")
        ids1 = sorted([q["id"] for q in r1.json()["questions"]])
        ids2 = sorted([q["id"] for q in r2.json()["questions"]])
        assert ids1 == ids2

    def test_daily_status_requires_auth(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/daily-practice/status")
        assert r.status_code == 401

    def test_daily_status_not_completed_initially(self, api_client, auth_headers):
        r = api_client.get(f"{BASE_URL}/api/daily-practice/status", headers=auth_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["completed"] is False

    def test_daily_status_completed_after_submit(self, api_client, auth_headers):
        daily = api_client.get(f"{BASE_URL}/api/daily-practice").json()
        answers = [{"question_id": q["id"], "selected": q["answer_index"]} for q in daily["questions"]]
        submit = api_client.post(
            f"{BASE_URL}/api/quiz/submit",
            json={"chapter_id": "daily", "answers": answers},
            headers=auth_headers,
        )
        assert submit.status_code == 200
        assert submit.json()["percent"] == 100.0

        status = api_client.get(f"{BASE_URL}/api/daily-practice/status", headers=auth_headers)
        body = status.json()
        assert body["completed"] is True
        assert body["percent"] == 100.0
        assert body["correct"] == 10
        assert body["total"] == 10

        # Ensure daily chapter does NOT show up in /api/progress (chapter-only filter)
        prog = api_client.get(f"{BASE_URL}/api/progress", headers=auth_headers)
        chapter_ids = [p["chapter_id"] for p in prog.json()]
        assert "daily" not in chapter_ids
