/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50716
Source Host           : localhost:3306
Source Database       : common

Target Server Type    : MYSQL
Target Server Version : 50716
File Encoding         : 65001

Date: 2020-02-22 17:02:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for anjuke_secondhand_house
-- ----------------------------
DROP TABLE IF EXISTS `anjuke_secondhand_house`;
CREATE TABLE `anjuke_secondhand_house` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `total_price` decimal(10,2) DEFAULT NULL,
  `total_price_unit` varchar(255) DEFAULT NULL,
  `avg_price` decimal(10,2) DEFAULT NULL,
  `avg_price_unit` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `house_type` varchar(255) DEFAULT NULL,
  `building_area` double(255,0) DEFAULT NULL,
  `building_area_unit` varchar(255) DEFAULT NULL,
  `floor` varchar(255) DEFAULT NULL,
  `building_time` varchar(255) DEFAULT NULL,
  `community` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `advantage` varchar(255) DEFAULT NULL,
  `salesman` varchar(255) DEFAULT NULL,
  `url` longtext,
  `url_md5` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
