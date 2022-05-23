from apps.utils import random_key

SECRET_KEY = random_key()
# HOST = '120.46.133.140'
# PORT = '3306'
# DATABASE = 'blog1'
# USERNAME = 'root'
# PASSWORD = 'Zwh200012121@'
HOST = '114.55.252.134'
PORT = '3306'
DATABASE = 'blog1'
USERNAME = 'root'
PASSWORD = 'Blog@2022'


DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# drop if tables have existed
import pymysql as mysql

# con = mysql.connect(host=HOST, port=3306, user=USERNAME, passwd=PASSWORD, db=DATABASE, charset="utf8mb4")
# mycursor = con.cursor()
# mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
# mycursor.execute("show tables")
# lst = mycursor.fetchall()
# # for table in lst:
# #     mycursor.execute("drop table %s" % table)
# con.commit()
# con.close()
