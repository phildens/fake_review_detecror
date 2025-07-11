from fastapi import FastAPI, Request
from web_api.detector import FakeReviewDetector
from web_api.models import Review, MarketLink
from fastapi.responses import JSONResponse
import requests
from urllib.parse import urlparse, urlunparse

detector = FakeReviewDetector()
app = FastAPI()
def make_reviews_url(url: str) -> str:
    # Разбираем URL
    parsed = urlparse(url)
    if "reviews" in url:
        return url
    # Составляем новый URL: сохраняем схему, хост и путь, сбрасываем всё остальное
    base = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    # Добавляем /reviews, убирая возможный завершающий слэш
    return base.rstrip('/') + '/reviews'

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.get("/detect_one_review")
async def detect_one(review: Review):
    return detector.detect_one_review(review.text)


@app.get("/detect_review_from_link")
async def detect_list(url):
    url = "http://studcamp-scraper:8200/api/v1/parse_url"
    params = {
        "url": make_reviews_url(link),
        "limit": 20
    }
    response = requests.get(url, params=params)
    response_json = response.json()

    rewiews = list(response.json()['reviews'])
    detect_rewiev = detector.detect_list_review(rewiews)
    main_data_from_json = {"url" : response_json['url']}
    merged_dict = {**detect_rewiev, **main_data_from_json}

    headers = {"Access-Control-Allow-Origin": "*"}
    return JSONResponse(content=merged_dict, headers=headers)
