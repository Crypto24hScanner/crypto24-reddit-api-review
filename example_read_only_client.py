"""Illustrative Reddit observation shaping, with no network access.

This example is designed solely for an API-access application review.
It contains no credentials, private Crypto24 X code or production integration.
It does NOT access Reddit; an authorised API client would be implemented only
following approval under Reddit's then-current terms and requirements.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


@dataclass(frozen=True)
class PublicDiscussionObservation:
    observed_at_utc: str
    community: str
    asset: str
    mention_count: int
    engagement_count: int
    source: str = "reddit"


def summarise_approved_sample(
    community: str, asset: str, public_posts: list[Mapping[str, Any]]
) -> dict[str, Any]:
    """Summarise synthetic or separately authorised observations.

    A production pipeline would have separate data-minimisation, deduplication,
    deletion, rate-limit and retention controls. This intentionally demonstrates
    no API calls, authentication or ingestion of live Reddit content.
    """
    if not community or not asset:
        raise ValueError("community and asset are required")
    if len(public_posts) > 100:
        raise ValueError("review sample limit exceeded")
    engagement = sum(max(0, int(p.get("engagement", 0))) for p in public_posts)
    result = PublicDiscussionObservation(
        observed_at_utc=datetime.now(timezone.utc).isoformat(),
        community=community,
        asset=asset,
        mention_count=len(public_posts),
        engagement_count=engagement,
    )
    return asdict(result)


if __name__ == "__main__":
    synthetic_sample = [{"engagement": 3}, {"engagement": 8}]
    print(summarise_approved_sample("r/example", "EXAMPLE", synthetic_sample))
    print("Review demonstration only: no Reddit API calls performed.")
