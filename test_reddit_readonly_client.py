"""Offline tests: no Reddit traffic and no private project dependencies."""
import io
import json
import unittest
import urllib.error

from reddit_readonly_client import ReadOnlyRedditClient, RedditAPIError, main


class Response:
    def __init__(self, body, headers=None):
        self.body = io.BytesIO(json.dumps(body).encode())
        self.headers = headers or {}

    def read(self, n=-1):
        return self.body.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.body.close()


class ClientTests(unittest.TestCase):
    def new_client(self, observed, bodies):
        def opener(request, timeout=20):
            observed.append(request)
            return Response(bodies.pop(0))
        return ReadOnlyRedditClient("testid", "testsecret",
            "test:crypto24-review:v0.1 (by /u/test_account)",
            opener=opener, sleep=lambda _: None)

    def test_default_is_offline(self):
        self.assertEqual(main([]), 0)

    def test_live_rejected_without_explicit_approval(self):
        from unittest.mock import patch
        with patch.dict("os.environ", {"REDDIT_API_APPROVED": "false"}):
            self.assertEqual(main(["--live"]), 2)

    def test_read_only_request_construction(self):
        seen = []
        client = self.new_client(seen, [
            {"access_token": "synthetic", "expires_in": 3600},
            {"data": {"children": [
                {"data": {"created_utc": 123, "score": 4, "num_comments": 2}},
                {"data": {"created_utc": 124, "score": 7, "num_comments": 8}},
            ]}},
        ])
        result = client.public_listing("CryptoCurrency", "new", 2)
        self.assertEqual(result["sample_count"], 2)
        self.assertEqual(seen[0].get_method(), "POST")
        self.assertEqual(seen[1].get_method(), "GET")
        self.assertTrue(seen[1].full_url.startswith("https://oauth.reddit.com/r/CryptoCurrency/new?"))
        self.assertFalse(any("testsecret" in r.full_url for r in seen))

    def test_invalid_subreddit_rejected_before_network(self):
        seen = []
        client = self.new_client(seen, [])
        with self.assertRaises(ValueError):
            client.public_listing("../private", "new")
        self.assertEqual(seen, [])

    def test_comment_listing(self):
        seen = []
        client = self.new_client(seen, [
            {"access_token": "synthetic", "expires_in": 3600},
            {"data": {"children": [{"data": {"created_utc": 123, "score": 1, "body": "test"}}]}}
        ])
        result = client.public_listing("Bitcoin", "comments", 1)
        self.assertEqual(result["sample_count"], 1)
        self.assertIsNone(result["engagement_sample"][0]["num_comments"])
        self.assertIn("/comments?", seen[1].full_url)

    def test_deleted_content_omitted(self):
        seen = []
        client = self.new_client(seen, [
            {"access_token": "synthetic", "expires_in": 3600},
            {"data": {"children": [{"data": {"body": "[deleted]"}}, {"data": {"score": 2}}]}}
        ])
        self.assertEqual(client.public_listing("Bitcoin")["sample_count"], 1)

    def test_limit_validation(self):
        seen = []
        client = self.new_client(seen, [])
        for limit in (0, 26, True):
            with self.assertRaises(ValueError):
                client.public_listing("Bitcoin", limit=limit)
        self.assertEqual(seen, [])

    def test_missing_access_token_rejected(self):
        client = self.new_client([], [{"error": "invalid_client"}])
        with self.assertRaises(RedditAPIError):
            client.public_listing("Bitcoin")


if __name__ == "__main__":
    unittest.main()
