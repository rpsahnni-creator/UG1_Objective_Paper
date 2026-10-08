"""Backend API tests for Introduction to Computer & IT course app."""
import os
import pytest
import requests

BASE_URL = os.environ.get("EXPO_PUBLIC_BACKEND_URL") or "https://it-course-app.preview.emergentagent.com"
BASE_URL = BASE_URL.rstrip("/")

ADMIN_EMAIL = "kijitechnology@gmail.com"
ADMIN_PASSWORD = "admin@123"


@pytest.fixture(scope="module")
def api():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def admin_token(api):
    r = api.post(f"{BASE_URL}/api/auth/login",
                 json={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert r.status_code == 200, r.text
    return r.json()["token"]


@pytest.fixture(scope="module")
def guest_token(api):
    r = api.post(f"{BASE_URL}/api/auth/guest")
    assert r.status_code == 200, r.text
    return r.json()["token"]


# -------- Health --------
class TestHealth:
    def test_root(self, api):
        r = api.get(f"{BASE_URL}/api/")
        assert r.status_code == 200
        data = r.json()
        assert data.get("status") == "ok"


# -------- Auth --------
class TestAuth:
    def test_admin_login_success(self, api):
        r = api.post(f"{BASE_URL}/api/auth/login",
                     json={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["is_admin"] is True
        assert d["email"] == ADMIN_EMAIL
        assert isinstance(d["token"], str) and len(d["token"]) > 10

    def test_admin_login_bad_creds(self, api):
        r = api.post(f"{BASE_URL}/api/auth/login",
                     json={"username": ADMIN_EMAIL, "password": "wrongpass"})
        assert r.status_code == 401

    def test_guest_login(self, api):
        r = api.post(f"{BASE_URL}/api/auth/guest")
        assert r.status_code == 200
        d = r.json()
        assert d["is_admin"] is False
        assert d["email"].startswith("guest-")
        assert d["token"]

    def test_me_endpoint_admin(self, api, admin_token):
        r = api.get(f"{BASE_URL}/api/auth/me",
                    headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 200
        d = r.json()
        assert d["email"] == ADMIN_EMAIL
        assert d["is_admin"] is True

    def test_me_endpoint_guest(self, api, guest_token):
        r = api.get(f"{BASE_URL}/api/auth/me",
                    headers={"Authorization": f"Bearer {guest_token}"})
        assert r.status_code == 200
        assert r.json()["is_admin"] is False

    def test_me_endpoint_no_token(self, api):
        r = api.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code == 401


# -------- Chapters --------
class TestChapters:
    def test_list_chapters_returns_3(self, api):
        r = api.get(f"{BASE_URL}/api/chapters")
        assert r.status_code == 200
        chapters = r.json()
        assert isinstance(chapters, list)
        assert len(chapters) == 3
        ids = sorted(c["id"] for c in chapters)
        assert ids == ["unit1", "unit2", "unit3"]
        for c in chapters:
            assert c["name_en"] and c["name_hi"]
            assert c["description_en"] and c["description_hi"]
            assert isinstance(c["question_count"], int)
            assert c["question_count"] > 0, f"{c['id']} has 0 questions"


# -------- Study Material --------
class TestStudyMaterial:
    @pytest.mark.parametrize("cid", ["unit1", "unit2", "unit3"])
    def test_study_material_bilingual(self, api, cid):
        r = api.get(f"{BASE_URL}/api/chapters/{cid}/study-material")
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["chapter_id"] == cid
        assert d["title_en"] and d["title_hi"]
        assert isinstance(d["sections"], list) and len(d["sections"]) > 0
        for s in d["sections"]:
            assert s["heading_en"] and s["heading_hi"]
            assert s["body_en"] and s["body_hi"]

    def test_study_material_not_found(self, api):
        r = api.get(f"{BASE_URL}/api/chapters/unitX/study-material")
        assert r.status_code == 404


# -------- MCQs --------
class TestMCQs:
    @pytest.mark.parametrize("cid", ["unit1", "unit2", "unit3"])
    def test_mcqs_bilingual_structure(self, api, cid):
        r = api.get(f"{BASE_URL}/api/chapters/{cid}/mcqs?limit=50")
        assert r.status_code == 200
        qs = r.json()
        assert isinstance(qs, list) and len(qs) > 0
        assert len(qs) <= 50
        for q in qs[:5]:
            assert q["chapter_id"] == cid
            assert q["question_en"] and q["question_hi"]
            assert len(q["options_en"]) == 4
            assert len(q["options_hi"]) == 4
            assert 0 <= q["answer_index"] <= 3
            assert q["explanation_en"] and q["explanation_hi"]
            assert q["difficulty"]
            assert q["id"]


# -------- Quiz submit --------
class TestQuizSubmit:
    def test_submit_quiz_returns_breakdown(self, api, guest_token):
        # fetch 3 MCQs from unit1
        r = api.get(f"{BASE_URL}/api/chapters/unit1/mcqs?limit=3")
        assert r.status_code == 200
        qs = r.json()[:3]
        assert len(qs) == 3

        # Pick: 2 correct, 1 wrong
        answers = []
        for i, q in enumerate(qs):
            if i < 2:
                sel = q["answer_index"]
            else:
                sel = (q["answer_index"] + 1) % 4
            answers.append({"question_id": q["id"], "selected": sel})

        r = api.post(
            f"{BASE_URL}/api/quiz/submit",
            json={"chapter_id": "unit1", "answers": answers},
            headers={"Authorization": f"Bearer {guest_token}"},
        )
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["total"] == 3
        assert d["correct"] == 2
        assert d["wrong"] == 1
        assert abs(d["percent"] - (2 / 3 * 100)) < 0.01
        assert "details" in d and len(d["details"]) == 3

    def test_submit_quiz_requires_auth(self, api):
        r = api.post(f"{BASE_URL}/api/quiz/submit",
                     json={"chapter_id": "unit1", "answers": []})
        assert r.status_code == 401
