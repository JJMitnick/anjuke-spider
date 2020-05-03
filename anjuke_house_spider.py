# -*-coding:utf-8-*-
# @time: 2020/5/3 11:32
# @author: Mitnick
# @description: 安居客二手房爬虫

import hashlib
import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from time import sleep

from anjuke_house_pipeline import AnjukeHousePipeline
from log_helper import LogHelper
from settings import *


def is_late_at_night():
    hour = datetime.now().hour
    # 爬虫深夜也需要休息
    if hour >= 23 or hour < 9:
        return True
    return False


class AnjukeHouseSpider(object):
    def __init__(self):
        self.pipeline = AnjukeHousePipeline()
        self.md5_set = self.get_md5()
        self.log = LogHelper(log_file='log/anjuke.log', log_name='anjuke').get_logger()

    def spider(self):
        while True:
            if is_late_at_night():
                sleep(1000)
            for city in ANJUKE_CITY:
                url_city = INIT_URL.format(city)
                response = requests.get(url_city, headers=HEADERS).content.decode('utf8')
                soup = BeautifulSoup(response, 'lxml')
                span = soup.find('span', {'class': 'elems-l'})
                items = span.find_all('a')
                for item in items:
                    area_url = item.get('href')[0:-2]
                    area = item.get_text()
                    # 不抓取周边城市
                    if '周边' in area:
                        continue
                    for o in SEACHER_SORT:
                        for p in range(1, 51, 1):
                            url = '%s%s-p%s/#filtersort' % (area_url, o, p)
                            rsp = requests.get(url, headers=HEADERS).content.decode('utf8')
                            if '验证码必须填写' in rsp:
                                self.log.error('已被屏蔽，暂停抓取')
                                sleep(100000000)
                            save_flag = self.parse(rsp, city, area)
                            sleep_time = round(random.uniform(3, 7), 2)
                            sleep(sleep_time)
                            if not save_flag:
                                self.log.info('***** break circulation ******')
                                break
            self.log.info("run around and sleep 1800s")
            sleep(1800)

    def parse(self, response, city, area):
        soup = BeautifulSoup(response, 'lxml')
        house_list = soup.find_all('li', {'class': 'list-item'})
        # 判断该URL是否有没收录的房源
        flag = False
        for item in house_list:
            house_title_ = item.find('div', {'class': 'house-title'}).find('a')
            title = house_title_.get_text().strip()
            url = house_title_.get('href')

            details_item_list = item.find_all('div', {'class': 'details-item'})
            detail_first = details_item_list[0].find_all('span')
            house_type = detail_first[0].get_text() if len(detail_first) > 0 else ''
            building_area = detail_first[1].get_text().replace('m²', '') if len(detail_first) > 1 else ''
            floor = detail_first[2].get_text() if len(detail_first) > 2 else ''
            building_time = detail_first[3].get_text() if len(detail_first) > 3 else ''

            detail_second = details_item_list[1].find('span') if len(details_item_list) > 1 else ''
            if not detail_second:
                continue
            detail_second_text = detail_second.get_text().strip()
            dst_list = detail_second_text.split('\n')
            community = dst_list[0].strip() if len(dst_list) > 0 else ''
            address = dst_list[1].strip() if len(dst_list) > 1 else ''

            tags_bottom = item.find('div', {'class', 'tags-bottom'})
            tags_span = tags_bottom.find_all('span')
            advantage = ''
            for ts in tags_span:
                tag = ts.get_text()
                advantage = '%s|%s' % (advantage, tag)
            advantage = advantage[1:]

            broker = item.find('span', {'class': 'broker-name broker-text'})
            salesman = broker.get_text()

            price_det = item.find('span', {'class': 'price-det'})
            total_price = price_det.get_text().replace('万', '')

            unit_price = item.find('span', {'class': 'unit-price'})
            avg_price = unit_price.get_text().replace('元/m²', '')

            md5_str = '%s%s%s%s' % (community, house_type, building_area, total_price)
            hm = hashlib.md5()
            hm.update(md5_str.encode("utf8"))
            url_md5 = hm.hexdigest()
            save_result = self.save(total_price, avg_price, title, house_type, building_area, floor, building_time,
                                    community,
                                    city, area, address, advantage, salesman, url, url_md5)
            if not flag and save_result:
                flag = True
        return flag

    def save(self, total_price, avg_price, title, house_type, building_area, floor, building_time, community,
             city, area, address, advantage, salesman, url, url_md5):
        if url_md5 not in self.md5_set:
            self.pipeline.insert(total_price, avg_price, title, house_type, building_area, floor, building_time,
                                 community, city, area, address, advantage, salesman, url, url_md5)
            self.md5_set.add(url_md5)
            return True
        return False

    def get_md5(self):
        md5_set = set()
        query = self.pipeline.query_md5()
        for item in query:
            md5_set.add(item['url_md5'])
        return md5_set


if __name__ == '__main__':
    AnjukeHouseSpider().spider()
