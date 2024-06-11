from database import db
from datetime import datetime

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500))
    short_code = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.now())
    visit_count = db.Column(db.Integer, default=0)