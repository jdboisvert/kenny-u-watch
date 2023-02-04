from dataclasses import dataclass


@dataclass(frozen=True)
class KennyUPullListing:
    year: str
    make: str
    model: str
    date_listed: str
    row_id: str
    branch: str
    listing_url: str
    client_id: str
