# Proposed integration and compliance design

**Status:** Design for review only; live collection disabled pending Reddit API approval.

## Proposed flow

1. Obtain Reddit authorisation for the stated externally hosted, read-only, personal trading-research use case.
2. Store credentials outside source control using a restricted environment/secret management facility.
3. Retrieve only approved public posts and comments from permitted communities through documented API endpoints.
4. Store bounded observations needed to assess asset mention frequency, engagement changes, and coarse text sentiment; apply an explicit data-retention and deletion policy consistent with Reddit's requirements.
5. Generate private operator-facing research summaries, including caveats about sample coverage, promotional activity, sentiment confidence, and possible data gaps.

## Expected observations (subject to approval)

- Observation time (UTC), source community, target asset/ticker, post/comment identifier where necessary for deduplication and required deletions, public content timestamps, engagement measures, and limited text necessary for sentiment review.
- No collection of private messages, private subreddit content, or private user details.
- Usernames and profile information are not required for the intended analytical outputs and will be avoided unless Reddit requires a narrowly scoped operational purpose.

## Safety and operational controls

- **Access control:** Disabled-by-default collection; explicitly enable only after written approval and review of current terms.
- **Scope:** Read-only endpoints; configured communities and query bounds; no broad unrestricted scraping.
- **Rate limiting:** Honour the limits supplied for the approved application; handle HTTP 429 with bounded backoff and stop rather than circumventing restrictions.
- **Auditing:** Record request counts, failures, sampling gaps and relevant policy/deletion events without logging credentials or full response bodies.
- **Deletion/retention:** Maintain the ability to remove content/derived data as required by Reddit's current API terms and deletion guidance. Exact retention periods and allowed derivative uses to be confirmed during approval.
- **Security:** Never embed secrets in files committed to GitHub; no access tokens, servers, private project source, or trading API keys included in this review repository.
- **Scope control:** Reddit observations provide contextual alerts for human interpretation and cannot independently place trades.

## What is not claimed

This sample does **not** claim that API access has been approved, that any collection is currently running, that Reddit allows every proposed use, or that performance/rate limits have been validated. Implementation will be adapted to any conditions Reddit specifies.
