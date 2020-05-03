# -*-coding:utf-8-*-
# @time: 2020/5/3 11:42
# @author: Mitnick
# @description: 配置文件

##
# MySQL配置
##
MYSQL_CONNECTION = {"host": "localhost", "port": 3306, "user": "root", "pwd": "111111", "db": "anjuke"}

##
# 爬虫配置
##
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
}
INIT_URL = 'https://{0}.anjuke.com/sale/o1/'
# 抓取的城市，这是安居客定义的，一般是拼音的全拼
ANJUKE_CITY = ['guangzhou']
# 搜索排序：{5:最新, 4:价格升序, 3:价格降序, 2:面积升序, 1:面积降序}
SEACHER_SORT = [5, 4, 3, 2, 1]