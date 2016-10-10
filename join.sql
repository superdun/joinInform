CREATE DATABASE  IF NOT EXISTS `join` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `join`;
-- MySQL dump 10.13  Distrib 5.5.52, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: join
-- ------------------------------------------------------
-- Server version	5.5.52-0ubuntu0.14.04.1

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
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `summary` varchar(2550) DEFAULT NULL,
  `former_teachers` varchar(500) DEFAULT NULL,
  `present_teacher_id` int(255) DEFAULT NULL,
  `create_time` varchar(255) DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  `hours_per_class` float(255,1) unsigned zerofill DEFAULT '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000.0',
  `fee_per_class` float(255,1) unsigned zerofill DEFAULT '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000.0',
  `modules` varchar(2550) DEFAULT NULL,
  `present_class` int(255) DEFAULT '0',
  `total_class` int(255) DEFAULT '1',
  `active` int(1) DEFAULT '1',
  `dates` varchar(2550) DEFAULT NULL,
  `records` varchar(2550) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `teancher.id` (`present_teacher_id`),
  CONSTRAINT `teancher.id` FOREIGN KEY (`present_teacher_id`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'机器人A',NULL,'aa',12,NULL,NULL,0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001.5,0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000500.0,'m1,m2,m3,m4,m5',2,5,1,'06/15/2016, 09/01/2016, 11/02/2016, 12/06/2016, 12/16/2016','{\"12/16/2016\": {\"students\": [1], \"comment\": \"\\u6c5f\\u82cf\\u82cf\\u5dde\"}}'),(2,'机器人B','asdad',NULL,11,NULL,NULL,0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001.5,0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200.0,'m1,m2,m3,m4,m5',1,5,1,'06/15/2016, 09/01/2016, 11/02/2016, 12/06/2016, 12/16/2016','{\"12/16/2016\":{\"students\":[2],\"comment\":\"江苏苏州\"}}');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin',NULL),(2,'teacher',NULL);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_teacher`
--

DROP TABLE IF EXISTS `role_teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_teacher` (
  `role_id` int(255) DEFAULT NULL,
  `teacher_id` int(255) DEFAULT NULL,
  KEY `teacherId` (`teacher_id`),
  KEY `roleId` (`role_id`),
  CONSTRAINT `roleId` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `teacherId` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_teacher`
--

LOCK TABLES `role_teacher` WRITE;
/*!40000 ALTER TABLE `role_teacher` DISABLE KEYS */;
INSERT INTO `role_teacher` VALUES (NULL,NULL),(1,11),(2,12);
/*!40000 ALTER TABLE `role_teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chinese_name` varchar(255) DEFAULT NULL,
  `alias_names` varchar(255) DEFAULT NULL,
  `gender` int(1) DEFAULT NULL,
  `birthday` varchar(255) DEFAULT NULL,
  `grade` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `adress` varchar(255) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `former_courses` varchar(255) DEFAULT NULL,
  `create_time` varchar(255) DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  `present_course_id` int(255) DEFAULT NULL,
  `former_hours` float(255,1) DEFAULT '0.0',
  `present_class` varchar(255) DEFAULT NULL,
  `former_fee` float(255,1) DEFAULT '0.0',
  `fomer_discount` float(255,0) DEFAULT '0',
  `present_discount` varchar(255) DEFAULT '0',
  `attend_records` varchar(15000) DEFAULT NULL,
  `comment` varchar(2550) DEFAULT NULL,
  `account` varchar(45) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `course.id` (`present_course_id`),
  CONSTRAINT `course.id` FOREIGN KEY (`present_course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'学生1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,'{\"null\": {\"courseId\": 1, \"comment\": \"\"}}',NULL,'0'),(2,'学生2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,2,NULL,NULL,NULL,NULL,NULL,'{}',NULL,'0'),(3,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0.0,NULL,0.0,0,'0','',NULL,'0');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chinese_name` varchar(255) DEFAULT NULL,
  `alias_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `password` varchar(555) DEFAULT NULL,
  `history` varchar(2550) DEFAULT NULL,
  `comment` varchar(2550) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `total_hours` float DEFAULT '0',
  `stage_id` int(3) DEFAULT NULL,
  `prizes` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `active` int(255) DEFAULT '0',
  `confirm` int(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `stage.id` (`stage_id`),
  CONSTRAINT `stage.id` FOREIGN KEY (`stage_id`) REFERENCES `teacherstages` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (11,'管理员l','admin','admin',NULL,'$pbkdf2-sha512$25000$bI2RUgrBOKc0BqD0XiuFEA$1JoSq6IUh9XNJLCcvRA2sqG1cYOxozadi9nnam8Eqsblp0msXBEpQ6AT1PYsG9Ge9cQZ7weqSrS0y0iELBLBlA',NULL,NULL,NULL,0,1,NULL,'aa',1,1),(12,'老师ld',NULL,'teacher1',NULL,'$pbkdf2-sha512$25000$bI2RUgrBOKc0BqD0XiuFEA$1JoSq6IUh9XNJLCcvRA2sqG1cYOxozadi9nnam8Eqsblp0msXBEpQ6AT1PYsG9Ge9cQZ7weqSrS0y0iELBLBlA',NULL,NULL,NULL,1.5,1,NULL,'aaa',1,1),(15,NULL,NULL,'475098936@qq.com',NULL,'$pbkdf2-sha512$25000$MUao9Z5TypmT0lqL8R7j3A$3X3Lwrln6fCIAUaJclQXoRRFCycZyVJZZft.TttBFQGFVGSGXBvPe9fbAQZfapNL11.N3pCcuSTA1OvHeB3HmA',NULL,NULL,NULL,0,NULL,NULL,NULL,1,0),(16,'1231',NULL,NULL,NULL,'$pbkdf2-sha512$25000$K.UcAwAAgBACgFBKCQHA.A$UgRms7rQkUl.rQwXXuG.OYCLUn2sfdGdalGShh5GhNnZHp2z2KUeoofEbXKkgKaScDUT3gDiTYnRRL9/4dxiMg',NULL,NULL,NULL,0,1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacherstages`
--

DROP TABLE IF EXISTS `teacherstages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacherstages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `payment_per_hour` float(255,1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacherstages`
--

LOCK TABLES `teacherstages` WRITE;
/*!40000 ALTER TABLE `teacherstages` DISABLE KEYS */;
INSERT INTO `teacherstages` VALUES (1,'初级',80.0);
/*!40000 ALTER TABLE `teacherstages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-10 16:46:38
