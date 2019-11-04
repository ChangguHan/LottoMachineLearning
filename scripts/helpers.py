# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from scripts import Database
import json
import bcrypt
from flask import session

def get_session( ):
    return sessionmaker(bind=Database.engine)()

@contextmanager
def session_scope():

    s = get_session()
    s.expire_on_commit = False
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()



def add_user(username, password, email) :
    with session_scope() as s:
        u = Database.User(username=username, password=password.decode('utf8'), email = email)
        s.add(u)
        s.commit()

def check_username(username) :
    with session_scope() as s:
        return s.query(Database.User).filter(Database.User.username.in_([username])).first()

def add_originData(id, data_numbersJSON) :
    with session_scope() as s :
        u = Database.originData(id=id, data_numbers=data_numbersJSON)
        s.add(u)
        s.commit()

def check_originData(id):
    with session_scope() as s:
        return s.query(Database.originData.data_numbers).filter(Database.originData.id.in_([id])).first()


def add_predictedData(id, date_posted, learning_rate, steps, predicted_data) :
    with session_scope() as s :
        u = Database.predictedData(id=id, date_posted=date_posted, learning_rate=learning_rate, steps=steps, predicted_data=predicted_data)
        s.add(u)
        s.commit()

def check_predictedData(id) :
    with session_scope() as s :
        return s.query(Database.predictedData.predicted_data).filter(Database.predictedData.id.in_([id])).first()

def dbGetPredictedData(id, nums):
    # 데이터베이스에서 int list로 데이터받음
    with session_scope() as s:
        # 데이터베이스에서 데이터 받아서
        jsondata = s.query(Database.predictedData.predicted_data).filter(Database.predictedData.id == id).first()[0]
        dict = json.loads(jsondata)

        # 데이터형 바꿔줌
        newdict = dict[str(nums)]
        result = {}
        for i in newdict.keys() :
            result[str(i)] = str(newdict[i])

        return result

def dbGetOriginData(id):
    # 데이터베이스에서 int list로 데이터받음
    with session_scope() as s:
        # 데이터베이스에서 데이터 받아서
        string = s.query(Database.originData.data_numbers).filter(Database.originData.id == id).first()[0]

        # int로 나눠줌
        list_string = string[1:len(string)-1].split(',')
        result = []
        for i in list_string :
            result.append(int(i))

        return result

# 실질적으로 로그인 확인
def credential_valid(username, password) :
    with session_scope() as s :
        user = s.query(Database.User).filter(Database.User.username.in_([username])).first()
        # user = s.query(Database.User).filter(Database.User.username == username).first()

        if user :
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        else : return False

def get_user():
    username = session['username']
    with session_scope() as s :
        user = s.query(Database.User).filter(Database.User.username == username).first()
        return user

def hash_password(password) :
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def change_user(**kwargs) :
    username = session['username']
    with session_scope() as s :
        user = s.query(Database.User).filter(Database.User.username == username).first()
        for arg, val in kwargs.items() :
            if val != "":
                setattr(user, arg, val)
        s.commit()

def username_taken(username) :
    with session_scope() as s :
        return s.query(Database.User).filter(Database.User.username == username).first()