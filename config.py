from apps.utils import random_key

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'blog1'
USERNAME = 'root'
PASSWORD = 'Zwh200012121@'
SECRET_KEY = random_key()

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
