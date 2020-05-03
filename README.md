### 1. anjuke-spider
此项目的功能是抓取二手房的详细数据，爬虫使用requests库，数据存储使用MySQL

安居客的平台只能查看50页的数据，并且很多重复的数据，统计功能做得也比较烂，有些统计数据也许是不想我们看到的

写这爬虫的初衷是记录某一线城市的二手房的历史数据，并做一些数据分析

该爬虫已经稳定运行3个月，但是没有做绕过验证码的功能，所以建议抓取的频率建议使用默认的

### 2. 如何运行
#### 2.1 修改settings.py配置文件
* MySQL配置信息：MYSQL_CONNECTION
* 修改抓取城市：ANJUKE_CITY
* 修改搜索排序：SEACHER_SORT

#### 2.2 运行环境
* 安装python。使用python3以上版本
* 安装依赖：依赖信息在requirements.txt中
* 安装MySQL。使用MySQL5.7以上版本
* 建表：MySQL中执行anjuke_spider.sql文件

#### 2.3 启动爬虫
##### 2.3.1 Windows系统
* 第一种：双击start_show.bat，有弹框的
* 第二种：双击start_hidden.vbs，Windows后台运行
* 第三种：使用命令`python anjuke_house_spider.py`

##### 2.3.2 linux系统
* 使用命令：`python main.py &`









