import requests
import logging
import re
import json
from os import makedirs
from os.path import exists

# 设定logging格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 选择要爬取的网页及页数
BASE_URL = 'https://bangumi.tv/game/browser?sort=rank'
TOTAL_PAGE = 10
DIR = 'bangumi_games'
exists(DIR) or makedirs(DIR)

# 获取网页文本
def scraping_page(url):
    try:
        session = requests.Session()
        session.headers = {'user-agent': '114514'}
        response = session.get(url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        logging.error(f'Error occurred: {e}')

# 获取某一页的URL
def scraping_index(page):
    index_url = f'{BASE_URL}&page={page}'
    return scraping_page(index_url)

# 获取一个HTML页面上的游戏名
def parse_index(html):
    names = {}
    pattern = re.compile('<a href="/subject.*?class="l">(.*?)</a>')
    items = re.findall(pattern, html)
    decoded_items = [item.encode('latin-1').decode('utf-8') for item in items]
    for i, decoded_item in enumerate(decoded_items, start=1):
        key = f'name_{i}'
        names[key] = decoded_item
    return names

# 获取一个HTML页面上的游戏信息
def parse_detail(html):
    infos = {}
    pattern = re.compile(r'<p class="info tip">(.*?)</p>', re.S)
    items = re.findall(pattern, html)
    decoded_items = [item.encode('latin-1').decode('utf-8') for item in items]
    for i, decoded_item in enumerate(decoded_items, start=1):
        key = f'name_{i}'
        infos[key] = decoded_item
    return infos

# 将获取数据存储为json格式
def save(name, info):
    path = f'{DIR}/{name}.json'
    json.dump(info, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 主函数，将爬取到的信息存储为多个json
def main():    
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scraping_index(page)
        names = parse_index(index_html)
        infos = parse_detail(index_html)
        for name , info in zip(names.values(), infos.values()):
            save(name, info)
                    
if __name__ == '__main__':
    main()