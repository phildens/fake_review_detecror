from fastapi import FastAPI
from web_api.detector import FakeReviewDetector
from web_api.models import Review, MarketLink
detector = FakeReviewDetector()
app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.get("/detect_one_review")
async def detect_one(review: Review):
    return detector.detect_one_review(review.text)


@app.get("/detect_review_from_link")
async def detect_list(link: MarketLink):
    reviews = {"text":'отзыв1 '}
    return detector.detect_list_review(reviews)