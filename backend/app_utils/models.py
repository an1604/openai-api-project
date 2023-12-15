from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary


db = SQLAlchemy()

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String, db.ForeignKey('conversations.id'))
    user_input = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    processed = db.Column(db.Boolean, default=False)


class Conversations(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.String, primary_key=True)
    conversation_obj = db.Column(LargeBinary)
    history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Requests(db.Model):
    __tablename__ = 'requests'
    conversation_id = db.Column(db.String, primary_key=True)
    request_id = db.Column(db.String)


class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.String, primary_key=True)
    customer_name = db.Column(db.String)
    max_cd = db.Column(db.Integer)
    gender = db.Column(db.String)