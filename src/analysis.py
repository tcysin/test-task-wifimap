"""
Script for data aggregation and analysis.

There are some problems with this script: it does a lot of things, some
values are hard-coded, it is not customizable, etc. For the purposes of
demo we ignore them.
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

# TODO relative import?
from utils import (
    hotspots_by_user,
    hotspots_since,
    hotspots_with_location,
    hotspots_with_score,
)


def num_hotspots_by_user(user_id: int, df: pd.DataFrame):
    """Return how many hotspots a user has created."""

    hotspots = hotspots_by_user(user_id, df)
    return len(hotspots)


def num_hotspots_with_location(user_id: int, df: pd.DataFrame):
    """Return how many hotspots a user has created with the location set."""

    # hotspots created by this user
    hotspots = hotspots_by_user(user_id, df)

    # filter out hotspots without location
    hotspots = hotspots_with_location(hotspots)

    return len(hotspots)


def num_hotspots_since(user_id: int, df: pd.DataFrame, since: pd.Timestamp):
    """Return how many hotspots a user has created since the given timestamp."""

    # hotspots created by this user
    hotspots = hotspots_by_user(user_id, df)

    # hotspots created since given timestamp
    hotspots = hotspots_since(hotspots, since)

    return len(hotspots)


def num_hotspots_with_score(
    user_id: int, df: pd.DataFrame, lower=-float("inf"), upper=float("inf")
):
    """Return how many hotspots a user has created with the score between lower and upper bounds.

    The bounds are strict, NaN values are ignored.
    """

    # hotspots created by this user
    hotspots = hotspots_by_user(user_id, df)

    # select those within the bounds
    hotspots = hotspots_with_score(hotspots, lower, upper)

    return len(hotspots)


def num_hotspots_with_unique_connections(
    user_id: int,
    conns: pd.DataFrame,
    hotspots: pd.DataFrame,
    min_unique_conns: int = 1,
    since: pd.Timestamp = None,
):
    # get user's hotspots
    hotspots = hotspots_by_user(user_id, hotspots)
    logging.debug("User %s has %s hotspots.", user_id, len(hotspots))
    # we only need their ids for selection
    ids = hotspots.loc[:, "id"]

    # get all connections to selected hotspots
    mask = conns.loc[:, "hotspot_id"].isin(ids)
    conns = conns.loc[mask, :]
    logging.debug("There were %s connections to these hotspots.", len(conns))

    # (optional) filter by timestamp
    if since is not None:
        mask = conns.loc[:, "connected_at"] >= since
        conns = conns.loc[mask, :]
        logging.debug(f"Update: %s connections since %s.", len(conns), since)

    # group by hotspot and count the number of unique installations
    grouped = conns.groupby("hotspot_id", axis="rows")
    s = grouped["installation_id"].nunique()
    # leave only those hotspots with sufficient conn counts
    s = s[s >= min_unique_conns]

    logging.debug(
        "Number of hotspots with more than %s unique connections: %s.",
        min_unique_conns,
        len(s),
    )

    return len(s)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run aggregation analysis on wifi-related data."
    )

    parser.add_argument(
        "uid",
        type=int,
        help="user ID",
    )
    parser.add_argument(
        "conns",
        type=Path,
        help="CSV file with connection logs",
    )
    parser.add_argument(
        "hotspots",
        type=Path,
        help="CSV file with wifi hotspots data",
    )
    parser.add_argument(
        "users",
        type=Path,
        help="CSV file with user data",
    )
    # TODO set logging level
    parser.add_argument(
        "--loglevel",
        default="warning",
        choices=["debug", "info", "warning"],
        help="set the level of log messages (default: warning)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # logging settings
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    logging.basicConfig(level=numeric_level)

    # load the data, convert to correct formats
    conns_df = pd.read_csv(
        args.conns,
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
    conns_df["connected_at"] = conns_df["connected_at"].dt.tz_localize("utc")
    logging.info("Loaded %s connection records.", len(conns_df))

    hotspots_df = pd.read_csv(
        args.hotspots,
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
    logging.info("Loaded %s hotspot records.", len(hotspots_df))

    users_df = pd.read_csv(
        args.users,
        dtype={"email": "string"},
        parse_dates=["created_at", "updated_at"],
    )
    logging.info("Loaded %s user records.", len(users_df))

    # validate user ID
    if args.uid not in users_df.loc[:, "id"].values:
        logging.error("User %s does not exist.", args.uid)
        sys.exit(1)
    uid = args.uid

    # 1 - сколько wifi точек (мы wifi записи еще называем hotspots) создал пользователь
    x = num_hotspots_by_user(uid, hotspots_df)
    print(f"User {uid} has created {x} hotspots.")

    # 2 - сколько hotpots у пользователя с привязкой к месту
    x = num_hotspots_with_location(uid, hotspots_df)
    print(f"With location: {x} hotspots.")

    # 3 - сколько hotspots пользователь создал
    now = pd.Timestamp.utcnow()
    print(f"Over time:")
    # за все время
    x = num_hotspots_by_user(uid, hotspots_df)
    print(f"  {x} hotspots total")
    # за последний месяц - simple, but wrong implementation of 30 days;
    month_ago = now - pd.to_timedelta("30 days")
    x = num_hotspots_since(uid, hotspots_df, since=month_ago)
    print(f"  {x} hotspots since {month_ago}")
    # неделю
    week_ago = now - pd.to_timedelta("7 days")
    x = num_hotspots_since(uid, hotspots_df, since=week_ago)
    print(f"  {x} hotspots since {week_ago}")

    # 4 - сколько у пользователя hotspots
    print(f"By score_v4:")
    # хороших (score_v4 > 0.6)
    l = 0.6
    x = num_hotspots_with_score(uid, hotspots_df, lower=l)
    print(f"  {x} hotspots with good score (>{l})")
    # средних hotspots (0.3 < score_v4 < 0.6)
    l, h = 0.3, 0.6
    x = num_hotspots_with_score(uid, hotspots_df, lower=l, upper=h)
    print(f"  {x} hotspots with average score ({l} - {h})")
    # плохих (score_v4  < 0.3)
    h = 0.3
    x = num_hotspots_with_score(uid, hotspots_df, upper=h)
    print(f"  {x} hotspots with bad score (<{l})")

    # 5 - сколько у пользователя hotspots к которым было больше
    # [1, 5, 10] уникальных(!) подключений за
    # все время
    # последний год - simple, but wrong implementation of 365 days
    # последний месяц
    # последнюю неделю.
    now = pd.Timestamp.utcnow()
    print(f"Hotspots with unique connections over time:")

    for min_unique_conns in [1, 5, 10]:
        for delta in ["365 days", "30 days", "7 days"]:
            since = now - pd.to_timedelta(delta)
            x = num_hotspots_with_unique_connections(
                uid, conns_df, hotspots_df, min_unique_conns, since
            )
            print(
                f"  {x} hotspots "
                f"with {min_unique_conns}+ unique connections "
                f"since {since}"
            )
