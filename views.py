# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect, flash, session, request, render_template, g
from modules import *
from copy import deepcopy

app = Flask(__name__)


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
    if not hasattr(g, 'db'):
        g.db = connect_db()
    if request.method == 'POST':
        user_id, session['error_info'] = check_register_info(deepcopy(request.form), g.db)
        if user_id:
            session['logged_in'] = True
            session['user_id'] = user_id
            del session['error_info']
            flash('注册成功')
            return redirect(url_for('home_page'))
        else:
            flash(session['error_info'])
            return redirect(url_for('register'))

    return render_template('register.html', error_info=session.get('error_info', ''))


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


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()
