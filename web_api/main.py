from fastapi import FastAPI, Request
from web_api.detector import FakeReviewDetector
from web_api.models import Review, MarketLink
from fastapi.responses import JSONResponse
import requests
from urllib.parse import urlparse, urlunparse
import time

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
    suka = "http://studcamp-scraper:8200/api/v1/parse_url"
    st_time = time.time()

    print()
    params = {
        "url": make_reviews_url(url),
        "limit": 20
    }
    response = requests.get(suka, params=params)
    response_json = response.json()
    print(response_json)
    print(time.time() - st_time)
    print("--------")
    st_time = time.time()
    rewiews = list(response.json()['reviews'])
    detect_rewiev = detector.detect_list_review(rewiews)
    main_data_from_json = {"url" : response_json['url']}
    merged_dict = {**detect_rewiev, **main_data_from_json}
    print(time.time() - st_time)
    headers = {"Access-Control-Allow-Origin": "*"}
    print(merged_dict)
    return JSONResponse(content=merged_dict, headers=headers)
