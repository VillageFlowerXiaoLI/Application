# -*- coding: utf-8 -*-

# from flask import Flask, url_for, redirect, flash, session, request, render_template, g
# import sqlite3
# from modules import *
from views import *
import os

app.secret_key = os.urandom(24)

# app.config.from_object('config')

if __name__ == '__main__':
    app.run(debug=True)
