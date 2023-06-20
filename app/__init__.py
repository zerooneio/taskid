from flask import Flask, session
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = 'pandaman'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sik'

mysql = MySQL(app)

from app import routes