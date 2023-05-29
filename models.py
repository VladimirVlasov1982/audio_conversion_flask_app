import uuid
from flask import request
from setup_db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), unique=True)
    access_token = db.Column(db.String(50), unique=True)

    def __init__(self, name: str) -> None:
        self.name = name
        self.access_token = str(uuid.uuid4())

    def __str__(self):
        return self.name


class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True)
    filename = db.Column(db.String(50))
    user_id = db.Column(db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('records', lazy=True))
    url = db.Column(db.String, unique=True, nullable=False)
    data = db.Column(db.LargeBinary)

    def __init__(self, filename: str, user_id: uuid, data: bytes) -> None:
        self.id = str(uuid.uuid4())
        self.filename = filename
        self.user_id = user_id
        self.data = data
        self.url = f'http://{request.host}/record?id={self.id}&user={self.user_id}'
