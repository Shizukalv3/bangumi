import mysql.connector
import re
import os
import json
from datetime import datetime
from gettime import get_time
from getplatform import get_platform
from getgenre import get_genre

# 建立MySQL连接
conn = mysql.connector.connect(
    host='localhost', #你的IP
    user='root', #你的用户名
    password='114514' #你的密码
)

cursor = conn.cursor()

# 若数据库不存在则新建
database = 'bangumi_games'
create_database_query = f'CREATE DATABASE IF NOT EXISTS {database}'
cursor.execute(create_database_query)

# 若表格不存在则新建
create_table_query = """
CREATE TABLE IF NOT EXISTS anime (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    release_date VARCHAR(100),
    genre VARCHAR(100),
    platform VARCHAR(100)
)
"""

insert_query = """
INSERT INTO anime (name, release_date,
                genre, platform) VALUES (%s, %s, %s, %s)
"""

cursor.execute(f'USE bangumi_games')
cursor.execute(create_table_query)

dir = './bangumi_games'

# 遍历同级目录下所有json文件，将获取数据写入数据库表格内
for filename in os.listdir(dir):
    if filename.endswith(".json"):
        with open(os.path.join(dir, filename), 'r', encoding='utf-8') as file:
            data = json.load(file)
            name = os.path.splitext(filename)[0]
            match = get_time(data)
            if match:
                try:
                    release_date = datetime.strptime(match[0], "%Y-%m-%d").strftime("%Y-%m-%d")
                    release_date = release_date[0]
                except ValueError:
                    release_date = match
                    release_date = release_date[0]
            else:
                release_date = None
            platform = get_platform(data)
            genre = get_genre(data)
            cursor.execute(insert_query, (name, release_date, genre, platform))

# 关闭连接
conn.commit()
cursor.close()
conn.close()


