"""
twitter_api.py – Twitter / X API integration for Yeonkkachi.

Handles authenticated posting and fetching of tweets related to
the bot's trading activity for full public transparency.

Environment variables required (set in a .env file, never commit them):
    TWITTER_API_KEY
    TWITTER_API_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET
    TWITTER_BEARER_TOKEN
"""

import os
from typing import Optional

import tweepy
from dotenv import load_dotenv

from bot.logger import get_logger

load_dotenv()
log = get_logger("twitter_api")


def _build_client() -> tweepy.Client:
    """Construct and return an authenticated Tweepy v2 Client."""
    return tweepy.Client(
        bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        wait_on_rate_limit=True,
    )


def post_tweet(text: str) -> Optional[str]:
    """Post *text* as a tweet and return the new tweet ID, or None on failure."""
    if len(text) > 280:
        log.warning("Tweet text exceeds 280 characters – it will be truncated.")
        text = text[:277] + "..."

    try:
        client = _build_client()
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        log.info(f"Tweet posted successfully (id={tweet_id})")
        return tweet_id
    except tweepy.TweepyException as exc:
        log.error(f"Failed to post tweet: {exc}")
        return None


def fetch_recent_tweets(query: str, max_results: int = 10) -> list[dict]:
    """Search recent tweets matching *query* and return a list of dicts."""
    try:
        client = _build_client()
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "author_id", "text"],
        )
        tweets = []
        if response.data:
            for tweet in response.data:
                tweets.append(
                    {
                        "id": tweet.id,
                        "text": tweet.text,
                        "created_at": str(tweet.created_at),
                        "author_id": tweet.author_id,
                    }
                )
        log.info(f"Fetched {len(tweets)} tweet(s) for query: '{query}'")
        return tweets
    except tweepy.TweepyException as exc:
        log.error(f"Failed to fetch tweets: {exc}")
        return []
