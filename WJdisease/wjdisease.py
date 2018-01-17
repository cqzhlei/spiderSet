from wjdd import *

# 获取疾病列表的浏览器
browserlist = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# browserlist = webdriver.Chrome()
# 等待
waitlist = WebDriverWait(browserlist,5)

# https://www.pinganwj.com/diseaseDetail/1012

# 设置虚拟浏览器的窗口大小

browserlist.set_window_size(1600, 900)

# 疾病列表url的部分
diseaselisturl='https://www.pinganwj.com/diseaseList/pg'


# 搜索疾病列表页面
def searchlist(url):
    try:
        # https://www.pinganwj.com/diseaseList/pg1
        browserlist.get(url)
        # 等待下一页按钮可用
        submit = waitlist.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#try > div.mainbody.clearfix > div > div:nth-child(1) > div.page-list.clearfix > span.next-page')))
        # 获取每种疾病的链接
        get_links()

    except TimeoutError:
        # 需要调整
        searchlist()

def get_links():
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content-wrapper')))
    html = browserlist.page_source
    # print(html)
    doc = pq(html)
    # print('==============================================')
    items = doc('.news-list').items()
    # print(items)
    for item in items:
        # 获取疾病的链接
        ddlink = item.find('a').attr('href')
        # print(ddlink)
        # 搜索疾病的具体信息
        searchdd(ddlink)

# 补全疾病列表页面的url
def pageUrl(i):
    return diseaselisturl+str(i)


def main():
    # 眼睛观测的 平安万家 只有680个疾病列表的网页
    for i in range(2,  681):
        print('正在爬取第'+str(i)+'页')
        searchlist(pageUrl(i))

if __name__ == '__main__':
    main()