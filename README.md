# Crypto24 X — Reddit Data API Access Review

This standalone repository documents a **proposed** Reddit Data API integration for a private, externally hosted cryptocurrency market-research application. It is provided to support an API access request. It is **not** the production source repository, a live deployment, or evidence of approved Reddit API access.

## Purpose

Subject to Reddit's approval and applicable terms, the proposed integration would read public posts and comments in relevant cryptocurrency communities, measure changes in asset mentions and discussion engagement, and provide contextual sentiment and suspected-promotion warnings for an individual operator's market research.

The application supports **personal cryptocurrency trading research**; Reddit observations would be supplementary operator intelligence, not an autonomous trade trigger. No Reddit content is intended to be sold or used to train AI models.

## Intended community coverage

Initial public communities, subject to permission and policy: `r/CryptoCurrency`, `r/Bitcoin`, `r/ethereum`, `r/solana`, and `r/defi`. Scope may change as approved. Private/restricted content would not be accessed without authorisation.

## Platform activity

- **Read-only:** No posts, comments, votes, direct messages, moderator actions, or engagement manipulation.
- **External processing:** Analysis takes place in independently hosted Python software, not a Reddit-native interactive application.
- **Data minimisation:** Collect only fields needed for time-series mention/engagement analysis and short-term review; avoid storing user profiles or unnecessary personal information.
- **Responsible usage:** Implement Reddit-specified authentication, rate limits, retry/backoff, data retention and deletion handling, and any additional conditions imposed by approval.
- **Access gate:** No live Reddit collection will occur until approval is obtained and required credentials are provisioned securely.

## Why external Data API access rather than Devvit?

The use case is a Python-based research workflow that analyses public discussion signals alongside independently obtained market data and produces private reports outside Reddit. A Reddit-hosted community application is not the intended deployment model. We are requesting guidance and approval for this external read-only use case, rather than claiming Devvit cannot support any of its underlying functions.

## Contents

- [`INTEGRATION_DESIGN.md`](INTEGRATION_DESIGN.md): Proposed API operations, data handling and safeguards.
- [`reddit_readonly_client.py`](reddit_readonly_client.py): Functional, read-only OAuth API client with an approval gate (no live requests made).\n- [`test_reddit_readonly_client.py`](test_reddit_readonly_client.py): Offline tests using synthetic responses.\n- [`API_REVIEW_SCOPE.md`](API_REVIEW_SCOPE.md): Source-code scope, safety gates and implementation limitations.\n- [`example_read_only_client.py`](example_read_only_client.py): Earlier non-networked observation example.

## Important boundaries

This is a stand-alone disclosure sample. It does not contain proprietary trading strategies, internal architecture, exchange integrations, operational infrastructure, secrets, account identifiers, or material copied from the private Crypto24 X codebase. The application has not received Reddit API approval as of this publication.

## Contact

For implementation details, API eligibility, and any applicable commercial/financial-use classification, please respond through the associated Reddit Data API access request.
