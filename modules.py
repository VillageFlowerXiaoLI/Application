# -*- coding: utf-8 -*-

import sqlite3

db_path = '/Users/duxinlu/Desktop/dachuang2017/dachuang.db'


def connect_db():
    try:
        db = sqlite3.connect(db_path)
    except:
        raise

    return db


def confirm_user(username, password, db):
    cursor = db.cursor()

    sql = 'select id,username,password from users where username=?'
    result = cursor.execute(sql, (username,))
    user = result.fetchall()

    if not user:
        return (False, None)
    elif password == user[0][2]:
        return (True, user[0][0])
    else:
        return (False, None)


def get_user_info(user_id, db):
    cursor = db.cursor()

    sql = 'select * from users where id=?'
    result = cursor.execute(sql, (user_id,))
    user_info = result.fetchall()
    user_dict = {}

    if len(user_info) == 0:
        return None
    else:
        # user_dict['id'] = user_info[0][0]
        user_dict['username'] = user_info[0][1]
        # user_dict['password'] = user_info[0][2]
        user_dict['nickname'] = user_info[0][3]
        user_dict['sex'] = user_info[0][4]
        user_dict['birthday'] = user_info[0][5]
        user_dict['email'] = user_info[0][6]
        user_dict['phone_number'] = user_info[0][7]
        user_dict['head_img'] = user_info[0][8]
        return user_dict


# 检查用户注册信息是否合法,合法就入库,返回id+err_info(None),不合法返回None+err_info
def check_register_info(form, db):
    cursor = db.cursor()
    sql_username = 'select username from users where username=?'
    username = cursor.execute(sql_username, (form['username'],)).fetchall()
    if username:
        return (None, u'用户名已存在')
    username = form['username']
    password = form['password']
    confirm_password = form['confirm_password']
    if password != confirm_password:
        return (None, u'两次输入的密码不一致')
    nickname = form['nickname']
    sex = form['sex']
    birthday = form.get('birthday', 'NULL')
    email = form.get('email', 'NULL')
    phone_number = form['phone_number']

    sql = 'insert into users (username,password,nickname,sex,birthday,email,phone_number) values (?,?,?,?,?,?,?)'
    cursor.execute(sql, (username, password, nickname, sex, birthday, email, phone_number))
    db.commit()
    id = cursor.execute('select id from users where username=?', (username,)).fetchall()[0][0]
    return (id, None)
