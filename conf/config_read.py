import configparser
import os

project_dir = os.path.dirname(os.path.abspath('conf'))  # 获取当前文件的目录
config_path = os.path.join(project_dir, "conf", "config.ini")
cf = configparser.ConfigParser()
cf.read(config_path)  # 读取配置文件

# secs = cf.sections()   # 获取ini文件中的所有section，并以列表形式返回

# mysql_options = cf.options("MySQL") #获取某个section名所对应的键

# mysql_items = cf.items("MySQL")  # 获取section对应的全部键值对

host = cf.get("MySQL", "host")
user = cf.get("MySQL", "user")
password = cf.get("MySQL", "password")
db = cf.get("MySQL", "db")
charset = cf.get("MySQL", "charset")
port = cf.get("MySQL", "port")

sql = {
    'HOST' : host,
    'USER' : user,
    'PASSWORD' : password,
    'DB' : db,
    'CHARSET' : charset,
    'PORT' : port
}

