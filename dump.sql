-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: ihome
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `area_info`
--

DROP TABLE IF EXISTS `area_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `area_info` (
  `ai_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '城市id',
  `ai_name` varchar(32) NOT NULL COMMENT '城市名',
  `ai_ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`ai_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COMMENT='城市信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `house_faci_type`
--

DROP TABLE IF EXISTS `house_faci_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `house_faci_type` (
  `hft_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '设施类型id',
  `hft_name` varchar(32) NOT NULL COMMENT '设施名称',
  `hft_ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`hft_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COMMENT='设施类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `house_facilities`
--

DROP TABLE IF EXISTS `house_facilities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `house_facilities` (
  `hf_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '设施id',
  `hf_type` int(11) NOT NULL COMMENT '设施类型id',
  `hf_house` int(11) NOT NULL COMMENT '所属房屋id',
  `hf_ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`hf_id`),
  KEY `hf_type` (`hf_type`),
  KEY `hf_house` (`hf_house`),
  CONSTRAINT `house_facilities_ibfk_1` FOREIGN KEY (`hf_type`) REFERENCES `house_faci_type` (`hft_id`),
  CONSTRAINT `house_facilities_ibfk_2` FOREIGN KEY (`hf_house`) REFERENCES `house_info` (`hi_id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8 COMMENT='配套设施表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `house_image`
--

DROP TABLE IF EXISTS `house_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `house_image` (
  `him_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '房屋图片id',
  `him_house` int(11) NOT NULL COMMENT '所属房屋id',
  `him_image` varchar(128) NOT NULL COMMENT '房屋图片',
  `him_ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`him_id`),
  KEY `him_house` (`him_house`),
  CONSTRAINT `house_image_ibfk_1` FOREIGN KEY (`him_house`) REFERENCES `house_info` (`hi_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='房屋图片表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `house_info`
--

DROP TABLE IF EXISTS `house_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `house_info` (
  `hi_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '房屋id',
  `hi_user` int(11) NOT NULL COMMENT '所属客户id',
  `hi_title` varchar(64) NOT NULL COMMENT '房屋标题',
  `hi_price` decimal(6,2) NOT NULL DEFAULT '0.00' COMMENT '房屋单价',
  `hi_area` int(11) NOT NULL COMMENT '所属城市id',
  `hi_address` varchar(512) NOT NULL DEFAULT '' COMMENT '房屋详细地址',
  `hi_count` tinyint(4) NOT NULL DEFAULT '1' COMMENT '房间数量',
  `hi_acreage` int(11) NOT NULL DEFAULT '0' COMMENT '房屋面积',
  `hi_type` varchar(32) NOT NULL DEFAULT '' COMMENT '房屋户型',
  `hi_num` int(11) NOT NULL DEFAULT '1' COMMENT '可容纳人数',
  `hi_beds` varchar(512) NOT NULL DEFAULT '' COMMENT '卧床配置',
  `hi_deposit` decimal(7,2) NOT NULL DEFAULT '0.00' COMMENT '押金数',
  `hi_min_day` int(11) NOT NULL DEFAULT '1' COMMENT '最少入住天数',
  `hi_max_day` int(11) NOT NULL DEFAULT '0' COMMENT '最长入住天数 0表示无限制',
  `hi_order_count` int(11) NOT NULL DEFAULT '0' COMMENT '房屋销量',
  `hi_verify` tinyint(4) NOT NULL DEFAULT '0' COMMENT '审核状态 0未审核 1审核未通过 2审核通过',
  `hi_isonline` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否上线',
  `hi_image` varchar(128) DEFAULT NULL COMMENT '房屋主图片',
  `hi_ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `hi_utime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `hi_isDelete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`hi_id`),
  KEY `hi_user` (`hi_user`),
  KEY `hi_area` (`hi_area`),
  CONSTRAINT `house_info_ibfk_1` FOREIGN KEY (`hi_user`) REFERENCES `user_info` (`ui_id`),
  CONSTRAINT `house_info_ibfk_2` FOREIGN KEY (`hi_area`) REFERENCES `area_info` (`ai_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='房屋信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_info`
--

DROP TABLE IF EXISTS `order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_info` (
  `oi_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '订单id',
  `oi_user` int(11) NOT NULL COMMENT '下单客户id',
  `oi_house` int(11) NOT NULL COMMENT '所属房屋id',
  `oi_start_day` date NOT NULL COMMENT '入住日期',
  `oi_end_day` date NOT NULL COMMENT '离开日期',
  `oi_count_day` int(11) NOT NULL COMMENT '入住天数',
  `oi_price` decimal(6,2) NOT NULL COMMENT '房屋单价',
  `oi_amount` decimal(9,2) NOT NULL COMMENT '订单总额',
  `oi_status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '订单状态 0待接单 1待支付 2已支付 3待评价 4已完成 5已取消 6拒接单',
  `oi_comment` text COMMENT '评论/备注',
  `oi_ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `oi_utime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`oi_id`),
  KEY `oi_user` (`oi_user`),
  KEY `oi_house` (`oi_house`),
  CONSTRAINT `order_info_ibfk_1` FOREIGN KEY (`oi_user`) REFERENCES `user_info` (`ui_id`),
  CONSTRAINT `order_info_ibfk_2` FOREIGN KEY (`oi_house`) REFERENCES `house_info` (`hi_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='订单信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_info` (
  `ui_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '客户id',
  `ui_title` varchar(32) NOT NULL COMMENT '用户名',
  `ui_tel` varchar(11) NOT NULL COMMENT '手机号',
  `ui_pwd` varchar(40) NOT NULL COMMENT '密码',
  `ui_name` varchar(32) DEFAULT NULL COMMENT '实名认证_姓名',
  `ui_card` varchar(20) DEFAULT NULL COMMENT '实名认证_身份证号',
  `ui_image` varchar(128) DEFAULT NULL COMMENT '头像链接',
  `ui_is_admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否是管理员',
  `ui_isDelete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否注销状态',
  `ui_ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `ui_utime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`ui_id`),
  UNIQUE KEY `ui_title` (`ui_title`),
  UNIQUE KEY `ui_tel` (`ui_tel`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='客户信息表';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-18 20:38:46
