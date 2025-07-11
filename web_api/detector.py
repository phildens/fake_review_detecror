from typing import Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification





class FakeReviewDetector:
    def __init__(self):
        model_name = ("SravaniNirati/bert_fake_review_detection")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        print("создание модели")

    def predict_fake_review(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        out_list = torch.softmax(outputs.logits, dim=-1).tolist()

        return {
            'is_fake': out_list[0][1] >= 0.5,
            'reliability': out_list[0][1]
        }

    def detect_one_review(self, rewiew: str) -> dict[str, bool | float]:

        return self.predict_fake_review(rewiew)

    def detect_list_review(self, data):
        output = list()
        counter = 0
        prob_sum = 0
        for review in data:
            precessed_review = self.predict_fake_review(review['review_body'])
            counter += 1
            prob_sum += precessed_review["reliability"]

            merged_dict = {**precessed_review, **review}
            output.append(merged_dict)
        output.sort(key=lambda x: x["reliability"], reverse=True)
        if counter > 3:
            crop_output = output[:3]

        else:
            crop_output = output
        return {"reviews": crop_output, "avg_reliability": prob_sum / counter}
