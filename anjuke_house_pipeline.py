# -*-coding:utf-8-*-
# @time: 2020/5/3 11:22
# @author: Mitnick
# @description: 持久层


from mysql_helper import MysqlHelper


class AnjukeHousePipeline(object):
    def __init__(self):
        self.mysql = MysqlHelper()

    def insert(self, total_price, avg_price, title, house_type, building_area, floor, building_time,
               community, city, area, address, advantage, salesman, url, url_md5):
        sql = """
            insert into anjuke_secondhand_house (total_price,total_price_unit,avg_price,avg_price_unit,title,
            house_type,building_area,building_area_unit,floor,building_time,community,
            city,area,address,advantage,salesman,url,url_md5)
            values (%s,'%s',%s,'%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
        """ % (total_price, '万', avg_price, '元/m²', title, house_type, building_area, 'm²', floor, building_time,
               community, city, area, address, advantage, salesman, url, url_md5)
        self.mysql.execute(sql)

    def query_md5(self):
        sql = "select url_md5 from anjuke_secondhand_house"
        return self.mysql.query(sql)
