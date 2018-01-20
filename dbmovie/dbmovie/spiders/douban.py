# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request

from dbmovie.items import DoubanItem


class DoubanSpider(Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com/top250']
    start_urls = ['https://movie.douban.com/top250/']

    start_url = 'https://movie.douban.com/top250/'

    def start_requests(self):
        yield Request(self.start_url, callback=self.parse)

    def parse(self, response):
        item = DoubanItem()
        movies = response.xpath('//div[@class="item"]')
        for movie in movies:
            # 名次
            item['ranking'] = movie.xpath('div[@class="pic"]/em/text()').extract()[0]
            # 片名 提取多个片名
            titles = movie.xpath('div[@class="info"]/div[1]/a/span/text()').extract()
            item['title'] = titles
            # 获取导演信息和演员信息
            info_director = movie.xpath('div[2]/div[2]/p[1]/text()[1]').extract()[0].replace(" ", "").replace("\n", "")
            item['director'] = info_director
            # 上映日期
            date = movie.xpath('div[2]/div[2]/p[1]/text()[2]').extract()[0].replace(" ", "").replace("\n", "").split("/")[0]
            # 制片国家
            country = movie.xpath('div[2]/div[2]/p[1]/text()[2]').extract()[0].replace(" ", "").replace("\n", "").split("/")[1]
            # 影片类型
            category = movie.xpath('div[2]/div[2]/p[1]/text()[2]').extract()[0].replace(" ", "").replace("\n", "").split("/")[2]
            item['date'] = date
            item['country'] = country
            item['category'] = category
            desc = movie.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if len(desc) != 0:  # 判断info的值是否为空，不进行这一步有的电影信息并没有会报错或数据不全
                item['desc'] = desc
            else:
                item['desc'] = ' '

            # item['desc'] = movie.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()').extract()[0]
            item['rating_num'] = movie.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            item['people_count'] = movie.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[4]/text()').extract()[0]
            yield item

        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, callback=self.parse, dont_filter=True)
