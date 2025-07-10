from typing import Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def prediction_decorator(original_func):
    def wrapper(text: str) -> dict:
        pred = original_func(text)
        return {
            'is_fake': pred[0][1] >= 0.5,
            'reliability': pred[0][1]
        }

    return wrapper


class FakeReviewDetector:
    def __init__(self):
        model_name = ("SravaniNirati/bert_fake_review_detection")

        # Загрузка токенизатора и модели

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        print("создание модели")

    @prediction_decorator
    def predict_fake_review(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        return torch.softmax(outputs.logits, dim=-1).tolist()

    def detect_one_review(self, rewiew: str) -> dict[str, bool | float]:
        return {"is_fake": True, "fake_prob": 0.85}

    def detect_list_review(self, reviews):
        output = list()
        counter = 0
        prob_sum = 0
        for review in reviews:
            precessed_review = self.detect_one_review(review)
            counter += 1
            prob_sum += precessed_review["fake_prob"]

            merged_dict = {**precessed_review, **review}
            output.append(merged_dict)

        return {"reviews": output[:3], "avg_reliability" : prob_sum / counter}
