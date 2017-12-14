from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from pyquery import PyQuery as pq
from config import *

import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# 获取疾病详细信息的浏览器
browserdd = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# browserdd = webdriver.Chrome()
browserdd.set_window_size(1600, 900)


waitdd = WebDriverWait(browserdd,5)

# 平安万家主页的网址
wjhomeurl = 'https://www.pinganwj.com'

# 具体疾病的详细页面
def searchdd(ddurl):
    try:
        browserdd.get(wjhomeurl+ddurl)
        # 等待
        waitdd.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#searchSubmit')))
        # 获取具体疾病的详细信息
        get_info()
    except TimeoutError:
        # 需要调整
        searchdd()

def get_info():
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.main-content .headline-1 .para')))
    html = browserdd.page_source
    doc = pq(html)
    diseasedetail = {
        'dname': doc('.name-main').text(),
        'ddtail': doc('.main-content .para').text()
    }
    save_to_mongo(diseasedetail)
    # print('正在获取' + doc('.name-main').text() + '的疾病信息')
    # print(doc('.main-content .para').text())

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到mongoDB成功', result)
    except:
        print('存储到MongoDB失败', result)
