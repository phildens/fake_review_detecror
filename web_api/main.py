from fastapi import FastAPI, Request
from web_api.detector import FakeReviewDetector
from web_api.models import Review, MarketLink
import requests

detector = FakeReviewDetector()
app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.get("/detect_one_review")
async def detect_one(review: Review):
    return detector.detect_one_review(review.text)


@app.get("/detect_review_from_link")
async def detect_list(link):
    url = "http://studcamp-scraper:8200/api/v1/parse_url"
    params = {
        "url": link,
        "limit": 20
    }
    response = requests.get(url, params=params)
    response_json = response.json()

    rewiews = list(response.json()['reviews'])
    detect_rewiev = detector.detect_list_review(rewiews)
    main_data_from_json = {"url" : response_json['url']}
    merged_dict = {**detect_rewiev, **main_data_from_json}
    return merged_dict
