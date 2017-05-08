# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect, flash, session, request, render_template, g
import sqlite3
import os
from copy import deepcopy

app = Flask(__name__)

app.secret_key = os.urandom(24)

# app.config.from_object('config')

db_path = '/Users/duxinlu/Desktop/dachuang2017/dachuang.db'


def connect_db():
    try:
        db = sqlite3.connect(db_path)
    except:
        raise

    return db


# 返回格式(bool,id)
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


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
        return (None, '用户名已存在')
    username = form['username']
    '''加一个功能 判断密码是否安全'''
    password = form['password']
    confirm_password = form['confirm_password']
    if password != confirm_password:
        return (None, '两次输入的密码不一致')
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


@app.route('/server_shutdown')
def server_shutdown():
    pass
    '''数据库炸了的重定向'''


@app.route('/')
def home_page():
    # 从数据库提取一波文章，传递给模板
    return render_template('home_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if not hasattr(g, 'db'):
        g.db = connect_db()

    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']
        login_status = confirm_user(input_username, input_password, g.db)
        if not login_status[0]:
            error = '用户名或密码不正确'
        else:
            session['logged_in'] = True
            session['user_id'] = login_status[1]
            flash('登录成功')
            return redirect(url_for('home_page'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('登出成功')
    return redirect(url_for('home_page'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error_info = ''
    if not hasattr(g, 'db'):
        g.db = connect_db()

    if request.method == 'POST':
        user_id, error_info = check_register_info(deepcopy(request.form), g.db)
        if user_id:
            session['logged_in'] = True
            session['user_id'] = user_id
            flash('注册成功')
            return redirect(url_for('home_page'))
        else:
            flash(error_info)
            return redirect(url_for('register'))

    return render_template('register.html', error_info=error_info)


@app.route('/articles')
def articles():
    pass
    '''展示热门文章'''


@app.route('/articles/<article_id>')
def article(article_id):
    pass
    '''根据数据库中article_id显示文章'''


@app.route('/travels/<travel_id>')
def travel(travel_id):
    pass
    '''根据游记id显示游记'''


@app.route('/user/<user_id>')
def user_space(user_id):
    if not hasattr(g, 'db'):
        g.db = connect_db()

    user_dict = get_user_info(user_id, g.db)

    if user_dict:
        return render_template('user_space.html', user_dict=user_dict)


@app.route('/user/<user_id>/profile')
def user_profile(user_id):
    pass
    '''用户资料'''


if __name__ == '__main__':
    app.run(debug=True)
