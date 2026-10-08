"""
Tests for NEW AEC Hindi Grammar course feature: topics listing, topic detail,
syllabus, stats, and the shared quiz engine (mcqs/quiz-submit) working for AEC
topic slugs (regression check for duplicate-mcq-id scoring bug).
"""
import os
import pytest
import requests

BASE_URL = (os.environ.get("EXPO_BACKEND_URL", "").rstrip("/")
            or os.environ.get("EXPO_PUBLIC_BACKEND_URL", "").rstrip("/"))


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


class TestAecTopics:
    def test_list_topics_total_25(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/aec/topics")
        assert r.status_code == 200
        topics = r.json()
        assert len(topics) == 25

    def test_unit_split_13_and_12(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/aec/topics")
        topics = r.json()
        unit1 = [t for t in topics if t["unit"] == 1]
        unit2 = [t for t in topics if t["unit"] == 2]
        assert len(unit1) == 13
        assert len(unit2) == 12

    def test_topic_fields_present(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/aec/topics")
        t = r.json()[0]
        for field in ["slug", "unit", "title", "subtitle", "question_count"]:
            assert field in t

    def test_filter_by_unit_query_param(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/aec/topics", params={"unit": 1})
        assert r.status_code == 200
        topics = r.json()
        assert len(topics) == 13
        assert all(t["unit"] == 1 for t in topics)

    def test_sandhi_topic_detail(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/aec/topics/sandhi")
        assert r.status_code == 200
        data = r.json()
        assert data["slug"] == "sandhi"
        assert data["question_count"] == 48
        assert len(data["sections"]) > 0
        # sections must have heading + blocks
        for s in data["sections"]:
            assert "heading" in s
            assert "blocks" in s
            assert isinstance(s["blocks"], list)

    def test_topic_not_found_404(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/aec/topics/does-not-exist-xyz")
        assert r.status_code == 404


class TestAecSyllabusAndStats:
    def test_syllabus(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/aec/syllabus")
        assert r.status_code == 200
        data = r.json()
        assert "objectives" in data and len(data["objectives"]) > 0
        assert "outcomes" in data and len(data["outcomes"]) > 0
        assert "units" in data and len(data["units"]) == 2
        units_by_num = {u["unit"]: u for u in data["units"]}
        assert units_by_num[1]["topic_count"] == 13
        assert units_by_num[2]["topic_count"] == 12

    def test_stats(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/aec/stats")
        assert r.status_code == 200
        data = r.json()
        assert data["topics"] == 25
        assert data["mcqs"] == 457
        assert data["shorts"] == 25
        assert data["descriptives"] == 25


class TestAecSharedQuizEngine:
    """AEC MCQs are stored in the shared `mcqs` collection; verify the existing
    quiz endpoints work generically for AEC topic slugs with no duplicate-id
    scoring bug (regression check)."""

    def test_sandhi_mcqs_count_48(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/chapters/sandhi/mcqs", params={"limit": 10000})
        assert r.status_code == 200
        mcqs = r.json()
        assert len(mcqs) == 48

    def test_sandhi_mcq_ids_unique_and_correct_format(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/chapters/sandhi/mcqs", params={"limit": 10000})
        mcqs = r.json()
        ids = [m["id"] for m in mcqs]
        assert len(ids) == len(set(ids)), "Duplicate MCQ ids found for AEC topic sandhi!"
        for i in ids:
            assert i.startswith("mcq-")

    def test_sandhi_mcq_bilingual_fields_present(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/chapters/sandhi/mcqs", params={"limit": 1})
        m = r.json()[0]
        assert m["question_en"] == m["question_hi"]
        assert m["options_en"] == m["options_hi"]

    def test_sandhi_quiz_submit_all_correct_scores_100(self, api_client, auth_headers):
        r = api_client.get(f"{BASE_URL}/api/chapters/sandhi/mcqs", params={"limit": 10000})
        mcqs = r.json()
        answers = [{"question_id": m["id"], "selected": m["answer_index"]} for m in mcqs]
        body = {"chapter_id": "sandhi", "answers": answers}
        r2 = api_client.post(f"{BASE_URL}/api/quiz/submit", json=body, headers=auth_headers)
        assert r2.status_code == 200
        result = r2.json()
        assert result["total"] == 48
        assert result["correct"] == 48
        assert result["wrong"] == 0
        assert result["percent"] == 100.0

    @pytest.mark.parametrize("slug,expected_count", [
        ("anaupcharik-patra", None),
        ("muhavare", None),
        ("nibandh-paryavaran", None),
        ("samas", None),
    ])
    def test_other_aec_topics_all_correct_100(self, api_client, auth_headers, slug, expected_count):
        r = api_client.get(f"{BASE_URL}/api/chapters/{slug}/mcqs", params={"limit": 10000})
        assert r.status_code == 200
        mcqs = r.json()
        if not mcqs:
            pytest.skip(f"No mcqs found for slug {slug} - check topic exists")
        ids = [m["id"] for m in mcqs]
        assert len(ids) == len(set(ids)), f"Duplicate MCQ ids for {slug}!"
        answers = [{"question_id": m["id"], "selected": m["answer_index"]} for m in mcqs]
        body = {"chapter_id": slug, "answers": answers}
        r2 = api_client.post(f"{BASE_URL}/api/quiz/submit", json=body, headers=auth_headers)
        assert r2.status_code == 200
        result = r2.json()
        assert result["percent"] == 100.0, f"Expected 100% for {slug}, got {result['percent']}"

    def test_all_457_aec_mcq_ids_globally_unique(self, api_client):
        """Cross-topic check: sum of per-topic mcqs across all 25 AEC topics == 457
        and no id collides across topics."""
        topics_r = api_client.get(f"{BASE_URL}/api/aec/topics")
        topics = topics_r.json()
        all_ids = []
        total_qc = 0
        for t in topics:
            r = api_client.get(f"{BASE_URL}/api/chapters/{t['slug']}/mcqs", params={"limit": 10000})
            mcqs = r.json()
            total_qc += len(mcqs)
            all_ids.extend([m["id"] for m in mcqs])
        assert total_qc == 457
        assert len(all_ids) == len(set(all_ids)), "AEC MCQ ids collide across topics!"


class TestNoRegressionOnSecChaptersEndpoint:
    """Light regression: /api/chapters should still return only the 3 SEC
    chapters (unit1/unit2/unit3), not AEC topics mixed in."""

    def test_chapters_endpoint_unaffected(self, api_client):
        r = api_client.get(f"{BASE_URL}/api/chapters")
        assert r.status_code == 200
        chapters = r.json()
        ids = {c["id"] for c in chapters}
        assert ids == {"unit1", "unit2", "unit3"}
