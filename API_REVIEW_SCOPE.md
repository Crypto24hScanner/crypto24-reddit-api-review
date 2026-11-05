# Source-code scope for Reddit reviewers

The `reddit_readonly_client.py` file is **functional API-accessing source code**, not merely pseudocode. It implements the OAuth client-credentials exchange and bounded GET requests for public `/r/{subreddit}/new` and `/r/{subreddit}/comments` listings using standard Python libraries.

**Safety gate:** Without `--live` the program performs no API requests. With `--live` but without `REDDIT_API_APPROVED=true`, it exits before accessing Reddit. The approval flag is a local safeguard, **not** evidence of official approval.

**No Reddit API access has been attempted or approved as part of publication.** No third-party account credentials are shared here.

**Local offline test:** `python3 -m unittest -v test_reddit_readonly_client.py`

**Data minimisation:** Example output includes timestamps and engagement counts, not post bodies, usernames, personal profiles or full Reddit responses. The client does not persist retrieved data.

**Honest limitations:** This small reference client does not yet perform full mention velocity or sentiment analysis. It also does not yet implement production deletion-event processing, durable caching, per-asset query design, comprehensive subreddit sampling or an evidence pipeline. Those capabilities, if authorised, would be implemented and validated separately under Reddit's current policies.

**Integration boundary:** This repository has no dependency on, credentials for, or connection to Crypto24 X, V7, GitHub automation or trading exchanges. It should be assessed as the narrow API interface proposed for a private research system.

**Developer-use case:** Private market intelligence for personal trading research, not academic research, resale, or a Reddit-hosted community application.
