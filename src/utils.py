"""
Utility functions for analysis of sample datasets.
"""

import pandas as pd


def hotspots_by_user(user_id: int, df: pd.DataFrame):
    """Return a df with hotspots that a user has created."""

    assert "owner_id" in df.columns, 'df must have "owner_id" column'

    mask = df.loc[:, "owner_id"] == user_id
    result = df.loc[mask, :]

    return result


def hotspots_with_location(df: pd.DataFrame):
    """Return a df with hotspots with the location present."""

    assert "foursquare_id" in df.columns, 'df must have "foursquare_id" column'
    assert "google_place_id" in df.columns, 'df must have "google_place_id" column'

    mask = df.loc[:, "foursquare_id"].notna() | df.loc[:, "google_place_id"].notna()
    result = df.loc[mask, :]

    return result


def hotspots_since(df: pd.DataFrame, since: pd.Timestamp):
    """Return a df with hotspots created since the given timestamp."""

    assert "created_at" in df.columns, 'df must have "created_at" column'
    assert since.tz is not None, "since must be an aware timestamp with a time zone"

    mask = df.loc[:, "created_at"] >= since
    result = df.loc[mask, :]

    return result


def hotspots_with_score(df: pd.DataFrame, lower=-float("inf"), upper=float("inf")):
    """Return a df with hotspots having `score_v4` value between lower and upper bounds.

    The bounds are strict, NaN values are ignored.
    """

    assert "score_v4" in df.columns, 'df must have "score_v4" column'
    assert lower < upper, "lower bound value must be smaller than upper"

    mask = (df["score_v4"] > lower) & (df["score_v4"] < upper)
    result = df.loc[mask, :]

    return result
