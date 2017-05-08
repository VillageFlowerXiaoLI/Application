# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect, flash, session, request, render_template, g
import sqlite3
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

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
    result = cursor.execute(sql, (username))
    user = result.fetchall()

    if len(user) == 0:
        return [False, None]
    else:
        if password == user[0][2]:
            return (True, user[0])


@app.route('/server_shutdown')
def server_shutdown():
    pass
    '''数据库炸了的重定向'''


@app.route('/')
def home_page():

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
            flash('登录成功')
            return redirect(url_for('home_page'))

    return render_template('login.html', error=error)


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
    pass
    '''显示用户的空间'''


@app.route('/user/<user_id>/profile')
def user_profile(user_id):
    pass
    '''显示用户资料，页面提供修改等操作'''


if __name__ == '__main__':
    app.run(debug=True)
