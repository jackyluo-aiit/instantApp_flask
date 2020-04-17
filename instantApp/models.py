# coding: utf-8
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from instantApp import db
from flask import jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Chatroom(db.Model):
    __tablename__ = 'chatrooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    chatroom_id = db.Column(db.ForeignKey('chatrooms.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    message_time = db.Column(db.DateTime, server_default=db.FetchedValue(), default=datetime.utcnow, index=True)

    chatroom = db.relationship('Chatroom', primaryjoin='Message.chatroom_id == Chatroom.id', backref='messages')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return {'chatroom_id': self.chatroom_id, 'user_id': self.user_id, 'name': self.name, 'message': self.message,
                'message_time': self.message_time.strftime('%Y-%m-%d %H:%M')}


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue(), default=datetime.utcnow, index=True)
    email = db.Column(db.String(254), unique=True)
    confirm = db.Column(db.Boolean, server_default=db.FetchedValue(), default=False)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    file_name = db.Column(db.String(200))
    file_path = db.Column(db.String(64), nullable=False)
    uploader = db.Column(db.String(20), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), default=datetime.utcnow, index=True)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return {'id': self.id, 'file_name': self.file_name, 'file_path': self.file_path, 'uploader': self.uploader,
                'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M')}
