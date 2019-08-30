# -*- coding: utf-8 -*-
import re
from spider_source.settings import decrypt_download_url
import scrapy


class MeipaiSpider(scrapy.Spider):
    name = 'meipai'
    allowed_domains = []
    start_urls = ['http://www.meipai.com/media/964816844?uid=1694687989&client_id=1089857302&utm_media_id=964816844&utm_source=meipai_share&utm_term=meipai_android&utm_content=test&viewCount=1&shareCount=1&gid=811757107']

    def xpath(self, html, xpath_):
        return html.xpath(xpath_).extract()

    def parse(self, response):
        # title_datas = self.xpath(response, '//h1/text()')
        # title = ''
        # for title_data in title_datas:
        #     if title_data.strip():
        #         title = title_data.strip()
        author_url_path = self.xpath(response, '//h3[@class="detail-name pa"]/a/@href')[0]
        publish_data = self.xpath(response, '//meta[@property="og:video:release_date"]/@content')[0].strip()
        publish_time = re.findall(r'(\d{4}-\d{2}-\d{2}).*(\d{2}:\d{2}:\d{2})', publish_data, re.S)[0]
        if len(publish_time) == 2:
            publish_time = '{} {}'.format(publish_time[0], publish_time[1])
        else:
            publish_time = publish_data
        categorys = self.xpath(response, '//a[@class="anchor"]/text()')
        category = ''
        for cate_data in categorys:
            if '首页' not in cate_data:
                category = cate_data.strip()
        item = dict(
            author_name=self.xpath(response, '//meta[@property="og:video:director"]/@content')[0].strip(),
            author_id=re.findall(r'user/(\d+)', author_url_path, re.S)[0],
            author_url='https://www.meipai.com' + author_url_path,
            author_avatar='https:' + self.xpath(response, '//img[@class="avatar pa detail-avatar"]/@src')[0],
            title=self.xpath(response, '//meta[@property="og:title"]/@content')[0].strip(),
            url=response.url,
            video_cover=self.xpath(response, '//meta[@property="og:image"]/@content')[0].strip(),
            video_duration=int(self.xpath(response, '//meta[@property="og:video:duration"]/@content')[0].strip()),
            publish_time=publish_time,
            tags=self.xpath(response, '//meta[@property="og:video:tag"]/@content')[0].strip(),
            video_url=decrypt_download_url(self.xpath(response, '//meta[@property="og:video:url"]/@content')[0]),
            video_width=self.xpath(response, '//meta[@property="og:video:width"]/@content')[0].strip(),
            video_height=self.xpath(response, '//meta[@property="og:video:height"]/@content')[0].strip(),
            play_count=int(self.xpath(response, '//meta[@itemprop="interactionCount"]/@content')[0].strip()),
            comment_count=int(self.xpath(response, '//span[@id="commentCount"]/text()')[0].strip()),
            digg_count=self.xpath(response, '//span[@class="pr top-2"]/text()')[0],
            category=category,
        )
        print(item)