# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect, flash, session, request, render_template, g
import sqlite3
import os

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

    if len(user) == 0:
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
        user_dict['phnoe_number'] = user_info[0][7]
        user_dict['head_img'] = user_info[0][8]
        return user_dict


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

    print user_id
    print user_dict

    if user_dict:
        return render_template('user_space.html', user_dict=user_dict)


@app.route('/user/<user_id>/profile')
def user_profile(user_id):
    pass
    '''用户资料'''


if __name__ == '__main__':
    app.run(debug=True)
