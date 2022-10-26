"""
Simple in-memory database.
"""

from pathlib import Path

import pandas as pd


DATA_DIR = Path().parent / "data"


# load the data, convert to correct formats
CONNS = pd.read_csv(
    DATA_DIR / "conns.csv",
    dtype={
        "foursquare_id": "string",
        "bssid": "string",
        "ssid": "string",
        "is_internet_available": bool,
        "is_protected": bool,
        "captive_portal_mode": "category",
        "match_type": "category",
    },
    parse_dates=["connected_at"],
)
# fix tz - set to UTC
CONNS["connected_at"] = CONNS["connected_at"].dt.tz_localize("utc")

HOTSPOTS = pd.read_csv(
    DATA_DIR / "hotspots.csv",
    dtype={
        "foursquare_id": "string",
        "google_place_id": "string",
        "name": "string",
        "ssid": "string",
        "bssid": "string",
        "country_code": "category",
    },
    parse_dates=["created_at", "updated_at", "deleted_at"],
)

USERS = pd.read_csv(
    DATA_DIR / "users.csv",
    dtype={"email": "string"},
    parse_dates=["created_at", "updated_at"],
)


def user_exists(user_id: int):
    return user_id in USERS.loc[:, "id"].values
