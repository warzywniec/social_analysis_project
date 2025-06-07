from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/social", tags=["REST - Exorde Social Media"])

class TweetIn(BaseModel):
    text: str
    created_at: datetime
    source: str = "unknown"
    lang: str = "und"
    label: str = "unlabeled"

@router.post("/tweets")
def receive_tweets(tweets: List[TweetIn]):
    print(f"[REST] Odebrano {len(tweets)} wpisów z social media.")
    for tweet in tweets[:3]:  # podgląd kilku
        print(f"[{tweet.source}] ({tweet.lang}) {tweet.created_at}: {tweet.text[:60]}...")
    return {"status": "ok", "received": len(tweets)}
