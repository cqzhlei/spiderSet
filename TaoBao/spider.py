import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from pyquery import PyQuery as pq
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# browser = webdriver.Chrome()
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

# 设置虚拟浏览器的窗口大小
browser.set_window_size(1600, 900)

wait = WebDriverWait(browser, 10)
def search():
    print('正在搜索')
    try:
        browser.get('https://s.taobao.com')
        #获取输入框
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        #获取搜索按钮
        #https://www.taobao.com中的selector不能用，但是https://s.taobao.com的selector可以使用===>???
        ##J_SearchForm > div > div.search-button > button
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_SearchForm > div > div.search-button > button')))
        # 输入美食
        input.send_keys(KEY_WORD)
        # 点击搜索按钮
        submit.click()
        # 等待获取页数
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutError:
        return search()
def next_page(page_number):
    print('正在翻页',page_number)
    # 页码输入框
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        # 页码提交按钮
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        # 清除页码框
        input.clear()
        # 重新填写页码框
        input.send_keys(page_number)
        # 页码确定按钮
        submit.click()
        # 等待页码高亮
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutError:
        next_page(page_number)
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()

        }
        print(product)
        # 取消注释就可以写入mongoDB中
        # save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到mongoDB成功', result)
    except:
        print('存储到MongoDB失败', result)


def main():
    try:
        # 获取总页码
        total = search()
        # 转换为数字
        total = int(re.compile('(\d+)').search(total).group(1))
        # 下一页
        for i in range(2, total+1):
            next_page(i)
    except Exception:
        print('出错了')
    finally:
        browser.close()

if __name__ == '__main__':
    main()


