from datetime import datetime

from flask import request

from . import db


MAX_SHORT_LENGTH = 16


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_short_url(self):
        return request.host_url + self.short

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_url(),
        )

    def from_dict(self, data):
        for field in data:
            setattr(self, field, data[field])
