"""
Marshmellow schemas for query args validation.
"""

from marshmallow import Schema
from marshmallow import fields, validate


class HotspotsQuerySchema(Schema):
    location = fields.Boolean(load_default=False)
    since = fields.DateTime(load_default=None)  # TODO make sure this has tz
    score_gt = fields.Float(load_default=None)
    score_lt = fields.Float(load_default=None)


class UniqueConnsQuerySchema(Schema):
    min_unique_conns = fields.Integer(
        load_default=1, validate=validate.Range(min=1, min_inclusive=True)
    )
    since = fields.DateTime(load_default=None)  # TODO make sure this has tz
