import pymysql

conn = pymysql.connect(
    host='120.46.133.140',  # 连接名称，默认127.0.0.1
    user='root',  # 用户名
    passwd='Zwh200012121@',  # 密码
    port=3306,  # 端口，默认为3306
    db='blog1',  # 数据库名称
    charset='utf8',  # 字符编码
)

print(conn)