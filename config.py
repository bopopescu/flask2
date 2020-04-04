# encoding: utf-8
# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'  # 要用的什么数据库
DRIVER = 'pymysql' # 连接数据库驱动
USERNAME = 'root'  # 用户名
PASSWORD ='123456'  # 密码
HOST = 'localhost'  # 服务器
PORT ='3306' # 端口
DATABASE = 'book' # 数据库名

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False