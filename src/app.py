"""
Minimal Flask app - RESTful API for analysis.
"""

import pandas as pd
from flask import abort, Flask, request
from marshmallow import ValidationError

from .db import user_exists
from .db import CONNS, HOTSPOTS
from .schemas import HotspotsQuerySchema, UniqueConnsQuerySchema
from .utils import (
    hotspots_by_user,
    hotspots_since,
    hotspots_with_location,
    hotspots_with_score,
)


# Flask stuff
app = Flask(__name__)


@app.route("/users/<int:user_id>/hotspots")
def describe_user_hotspots(user_id: int):
    if not user_exists(user_id):
        abort(404)

    # validate query params
    try:
        args = HotspotsQuerySchema().load(request.args)
    except ValidationError as err:
        abort(400, str(err.messages))

    location = args["location"]
    since = args["since"]  # datetime
    lower = args["score_gt"]
    upper = args["score_lt"]

    # get user's hotspots and filter them
    hotspots = hotspots_by_user(user_id, HOTSPOTS)
    app.logger.debug("User %s has %s hotspots.", user_id, len(hotspots))

    if location:
        hotspots = hotspots_with_location(hotspots)
        app.logger.debug("%s hotspots with location.", len(hotspots))

    if since is not None:
        hotspots = hotspots_since(hotspots, pd.to_datetime(since))
        app.logger.debug("%s hotspots since %s.", len(hotspots), since)

    # some scores may be NaN, so filter only when a bound is specified
    if (lower is not None) or (upper is not None):
        lower = -float("inf") if lower is None else lower
        upper = float("inf") if upper is None else upper
        hotspots = hotspots_with_score(hotspots, lower, upper)
        app.logger.debug(
            "%s hotspots with score between (%s, %s).", len(hotspots), lower, upper
        )

    count = len(hotspots)

    return {"count": count}


@app.route("/users/<int:user_id>/hotspots/unique_connections")
def describe_unique_connections(user_id: int):
    if not user_exists(user_id):
        abort(404)

    # validate query params
    try:
        args = UniqueConnsQuerySchema().load(request.args)
    except ValidationError as err:
        abort(400, str(err.messages))

    min_unique_conns = args["min_unique_conns"]
    since = args["since"]  # datetime

    # get number of unique connections
    hotspots = hotspots_by_user(user_id, HOTSPOTS)
    app.logger.debug("User %s has %s hotspots.", user_id, len(hotspots))

    ids = hotspots.loc[:, "id"]
    mask = CONNS.loc[:, "hotspot_id"].isin(ids)
    conns = CONNS.loc[mask, :]
    app.logger.debug("There were %s connections to these hotspots.", len(conns))

    if since is not None:
        mask = conns.loc[:, "connected_at"] >= since
        conns = conns.loc[mask, :]
        app.logger.debug(f"Update: %s connections since %s.", len(conns), since)

    # group by hotspot and count the number of unique installations
    grouped = conns.groupby("hotspot_id", axis="rows")
    s = grouped["installation_id"].nunique()
    # leave only those hotspots with sufficient conn counts
    s = s[s >= min_unique_conns]

    app.logger.debug(
        "Number of hotspots with more than %s unique connections: %s.",
        min_unique_conns,
        len(s),
    )

    count = len(s)

    return {"count": count}
