#!/usr/bin/env python3
"""Standalone, read-only Reddit Data API client for API-access review.

No production Crypto24 X code or credentials. Live requests require BOTH
--live and REDDIT_API_APPROVED=true; approval must actually be granted by Reddit.
Only public subreddit listings are requested. No usernames or content are stored.
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

AUTH_URL = "https://www.reddit.com/api/v1/access_token"
API_ORIGIN = "https://oauth.reddit.com"
SUBREDDIT = re.compile(r"^[A-Za-z0-9_]{2,21}$")
MAX_ITEMS = 25


class RedditAPIError(RuntimeError):
    pass


class ReadOnlyRedditClient:
    def __init__(self, client_id, client_secret, user_agent, *, opener=None, sleep=None):
        if not all((client_id, client_secret, user_agent)):
            raise ValueError("Client ID, client secret and user agent are required")
        if "by /u/" not in user_agent:
            raise ValueError("Use a descriptive User-Agent with Reddit account contact")
        self._id = client_id
        self._secret = client_secret
        self._ua = user_agent
        self._opener = opener or urllib.request.urlopen
        self._sleep = sleep or time.sleep
        self._token = None
        self._expiry = 0.0
        self._request_spacing = 1.5  # deliberately conservative, not an entitlement

    def _send(self, request):
        """Bounded retries; no request bodies or credentials printed to logs."""
        for attempt in range(3):
            try:
                with self._opener(request, timeout=20) as response:
                    data = response.read(2_000_001)
                    if len(data) > 2_000_000:
                        raise RedditAPIError("API response exceeds safety limit")
                    remaining = response.headers.get("X-Ratelimit-Remaining")
                    reset = response.headers.get("X-Ratelimit-Reset")
                    if remaining is not None and reset is not None:
                        try:
                            if float(remaining) < 2:
                                self._request_spacing = min(60.0, max(1.5, float(reset)))
                        except ValueError:
                            pass
                    return json.loads(data)
            except urllib.error.HTTPError as exc:
                if exc.code in (429, 500, 502, 503, 504) and attempt < 2:
                    retry_after = exc.headers.get("Retry-After") if exc.headers else None
                    try:
                        seconds = min(60.0, max(1.5, float(retry_after))) if retry_after else 2.0 * (attempt + 1)
                    except (ValueError, TypeError):
                        seconds = 2.0 * (attempt + 1)
                    self._sleep(seconds)
                    continue
                raise RedditAPIError(f"Reddit HTTP {exc.code}") from None
            except (urllib.error.URLError, TimeoutError) as exc:
                raise RedditAPIError(f"Reddit network error: {type(exc).__name__}") from None
            except (ValueError, UnicodeError) as exc:
                raise RedditAPIError("Invalid Reddit API JSON response") from None
        raise RedditAPIError("Reddit request retries exhausted")

    def _authenticate(self):
        if self._token and time.monotonic() < self._expiry:
            return
        auth = base64.b64encode(f"{self._id}:{self._secret}".encode()).decode("ascii")
        payload = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
        request = urllib.request.Request(
            AUTH_URL, data=payload, method="POST",
            headers={
                "Authorization": f"Basic {auth}",
                "User-Agent": self._ua,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        response = self._send(request)
        if not isinstance(response, dict) or not response.get("access_token"):
            raise RedditAPIError("OAuth response did not supply an access token")
        self._token = response["access_token"]
        self._expiry = time.monotonic() + min(3600, max(30, int(response.get("expires_in", 3600)) - 60))

    def public_listing(self, subreddit, kind="new", limit=10):
        """Fetch recent public posts or comments; return minimal counts only.

        Callers should not interpret a sampled listing as full conversation volume.
        No content is persisted by this review client.
        """
        if not SUBREDDIT.fullmatch(subreddit):
            raise ValueError("Invalid subreddit name")
        if kind not in ("new", "comments"):
            raise ValueError("Only new posts and public comments are supported")
        if not isinstance(limit, int) or isinstance(limit, bool) or not (1 <= limit <= MAX_ITEMS):
            raise ValueError("limit must be between 1 and 25")
        self._authenticate()
        query = urllib.parse.urlencode({"limit": limit, "raw_json": 1})
        url = f"{API_ORIGIN}/r/{subreddit}/{kind}?{query}"
        request = urllib.request.Request(
            url, headers={"Authorization": f"bearer {self._token}", "User-Agent": self._ua},
            method="GET",
        )
        self._sleep(self._request_spacing)
        response = self._send(request)
        try:
            children = response["data"]["children"]
            if not isinstance(children, list):
                raise TypeError()
        except (KeyError, TypeError):
            raise RedditAPIError("Unexpected Reddit listing shape") from None
        counts = []
        for obj in children:
            d = obj.get("data", {}) if isinstance(obj, dict) else {}
            if not isinstance(d, dict):
                continue
            if d.get("removed_by_category") or d.get("body") in ("[deleted]", "[removed]"):
                continue
            counts.append({
                "created_utc": d.get("created_utc"),
                "score": d.get("score"),
                "num_comments": d.get("num_comments") if kind == "new" else None,
            })
        return {"subreddit": subreddit, "type": kind, "sample_count": len(counts),
                "engagement_sample": counts, "coverage": "bounded listing; not exhaustive"}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only Reddit Data API review client")
    parser.add_argument("--live", action="store_true", help="Explicitly allow network requests (requires approval flag)")
    parser.add_argument("--subreddit", default="CryptoCurrency")
    parser.add_argument("--kind", choices=["new", "comments"], default="new")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args(argv)
    if not args.live:
        print("DISABLED: demonstration only. No Reddit requests made.")
        return 0
    if os.getenv("REDDIT_API_APPROVED", "").strip().lower() != "true":
        print("BLOCKED: explicit Reddit API approval not configured.", file=sys.stderr)
        return 2
    try:
        client = ReadOnlyRedditClient(
            os.environ["REDDIT_CLIENT_ID"],
            os.environ["REDDIT_CLIENT_SECRET"],
            os.environ["REDDIT_USER_AGENT"],
        )
        print(json.dumps(client.public_listing(args.subreddit, args.kind, args.limit)))
        return 0
    except (KeyError, ValueError, RedditAPIError) as exc:
        print(f"Collection unavailable: {type(exc).__name__}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
