# encoding:utf8

# 配置 app.config用于存储整个应用的配置变量，是一个字典

# 防止跨站请求伪造保护，CSRF（Cross-site request forgery）,要使用session，得先设置secret key，给cookie签名加密
DEBUG = True
SECRET_KEY = 'I am the secret_key !' 

USERNAME = 'root'
PASSWORD = 'mysql123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'guess_the_number'


SQLALCHEMY_DATABASE_URI = DATABASE_URL
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False


