from apps.util.common import random_key

HOST = '114.55.252.134'
PORT = '3306'
DATABASE = 'blog'
USERNAME = 'root'
PASSWORD = 'Blog@2022'
SECRET_KEY = random_key()

DB_URI = f"mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
