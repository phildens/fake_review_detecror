from pydantic import BaseModel


class Review(BaseModel):
    text: str


class MarketLink(BaseModel):
    url: str
