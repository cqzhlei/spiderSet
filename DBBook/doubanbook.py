import requests
import re
from pyquery import PyQuery as pq

content = requests.get('https://book.douban.com/').text
# doc = pq(content)
# print(doc('li'))
print(content)
pattern = re.compile('<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?</span>).*?year">(.*?)</span>.*?</li>',re.S)
results = re.findall(pattern,content)
print(results)
for result in results:
    url, name, author, date = result
    author = re.sub('\s', '', author)
    name = re.sub('\s', '',name)
    date = re.sub('\s', '', date)
    print(url, name, author, date)
