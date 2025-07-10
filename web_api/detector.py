from typing import Dict


class FakeReviewDetector:
    def __init__(self):
        print("создание модели")

    def detect_one_review(self, rewiew: str) -> dict[str, bool | float]:
        return {"is_fake": True, "fake_prob": 0.85}

    def detect_list_review(self, reviews):
        return {"reviews": [{'review_id': '123', "is_fake": True, "fake_prob": 0.85}]}
