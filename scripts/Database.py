# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
import sqlalchemy

SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
Base = declarative_base()

def db_connect():
    return create_engine(SQLALCHEMY_DATABASE_URI)

class predictedData(Base) :
    __tablename__ = 'predictedData'

    id = Column(Integer, primary_key = True)
    date_posted = Column(DateTime, nullable = False, default=datetime.utcnow())
    learning_rate = Column(Float, nullable = False)
    steps = Column(Integer, nullable = False)
    predicted_data = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Prediction ({self.id}) : ({self.date_posted})"

class originData(Base) :
    __tablename__ = 'originData'

    id = Column(Integer, primary_key = True)
    data_numbers = Column(JSON, nullable = False)


    def __repr__(self):
        return f"<originData ({self.id}),({self.data_numbers})"

class User(Base) :
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    username = Column(String(30), unique = True, nullable = False)
    email = Column(String(120), unique = True, nullable = False)
    password = Column(String(100), nullable = False)

    def __repr__(self) :
        return f"<User({self.id}','{self.username}','{self.email}')>"


engine = db_connect()
Base.metadata.create_all(engine)