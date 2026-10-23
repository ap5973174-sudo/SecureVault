
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Finding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    impact = db.Column(db.Text, nullable=False)
    remediation = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Open")
