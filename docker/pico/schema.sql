-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: localhost    Database: pico
-- ------------------------------------------------------
-- Server version	5.7.18-0ubuntu0.16.04.1

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
-- Table structure for table `alerts_alert`
--

DROP TABLE IF EXISTS `alerts_alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alerts_alert` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(25) NOT NULL,
  `body` varchar(160) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `read` tinyint(1) NOT NULL,
  `target_id` int(11),
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `alerts_alert_55e2df16` (`target_id`),
  KEY `alerts_alert_e8701ad4` (`user_id`),
  CONSTRAINT `alerts_alert_target_id_5c299758_fk_alerts_target_id` FOREIGN KEY (`target_id`) REFERENCES `alerts_target` (`id`),
  CONSTRAINT `alerts_alert_user_id_f5648313_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerts_alert`
--

LOCK TABLES `alerts_alert` WRITE;
/*!40000 ALTER TABLE `alerts_alert` DISABLE KEYS */;
/*!40000 ALTER TABLE `alerts_alert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alerts_target`
--

DROP TABLE IF EXISTS `alerts_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alerts_target` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL,
  `contest_id` int(11),
  `invite_id` int(11),
  `join_request_id` int(11),
  `team_id` int(11),
  `user_id` int(11),
  PRIMARY KEY (`id`),
  KEY `alerts_target_41b6de5d` (`contest_id`),
  KEY `alerts_target_28a44ea5` (`invite_id`),
  KEY `alerts_target_c158221d` (`join_request_id`),
  KEY `alerts_target_f6a7ca40` (`team_id`),
  KEY `alerts_target_e8701ad4` (`user_id`),
  CONSTRAINT `alerts_target_contest_id_32048aee_fk_contests_contest_id` FOREIGN KEY (`contest_id`) REFERENCES `contests_contest` (`id`),
  CONSTRAINT `alerts_target_invite_id_30a0a873_fk_teams_invite_id` FOREIGN KEY (`invite_id`) REFERENCES `teams_invite` (`id`),
  CONSTRAINT `alerts_target_join_request_id_0893c7a9_fk_teams_joinrequest_id` FOREIGN KEY (`join_request_id`) REFERENCES `teams_joinrequest` (`id`),
  CONSTRAINT `alerts_target_team_id_365f82c0_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`),
  CONSTRAINT `alerts_target_user_id_ddc04500_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerts_target`
--

LOCK TABLES `alerts_target` WRITE;
/*!40000 ALTER TABLE `alerts_target` DISABLE KEYS */;
/*!40000 ALTER TABLE `alerts_target` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add user',1,'add_user'),(2,'Can change user',1,'change_user'),(3,'Can delete user',1,'delete_user'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add log entry',4,'add_logentry'),(11,'Can change log entry',4,'change_logentry'),(12,'Can delete log entry',4,'delete_logentry'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can create contests',1,'create_contest'),(20,'Can add user profile',7,'add_userprofile'),(21,'Can change user profile',7,'change_userprofile'),(22,'Can delete user profile',7,'delete_userprofile'),(23,'Can add team',9,'add_team'),(24,'Can change team',9,'change_team'),(25,'Can delete team',9,'delete_team'),(26,'Can add invite',10,'add_invite'),(27,'Can change invite',10,'change_invite'),(28,'Can delete invite',10,'delete_invite'),(29,'Can add join request',11,'add_joinrequest'),(30,'Can change join request',11,'change_joinrequest'),(31,'Can delete join request',11,'delete_joinrequest'),(32,'Can add notification',12,'add_notification'),(33,'Can change notification',12,'change_notification'),(34,'Can delete notification',12,'delete_notification'),(35,'Can add submission',13,'add_submission'),(36,'Can change submission',13,'change_submission'),(37,'Can delete submission',13,'delete_submission'),(38,'Can add participant',14,'add_participant'),(39,'Can change participant',14,'change_participant'),(40,'Can delete participant',14,'delete_participant'),(41,'Can add problem',15,'add_problem'),(42,'Can change problem',15,'change_problem'),(43,'Can delete problem',15,'delete_problem'),(44,'Can add problem input',16,'add_probleminput'),(45,'Can change problem input',16,'change_probleminput'),(46,'Can delete problem input',16,'delete_probleminput'),(47,'Can add contest template',17,'add_contesttemplate'),(48,'Can change contest template',17,'change_contesttemplate'),(49,'Can delete contest template',17,'delete_contesttemplate'),(50,'Can add contest invite',18,'add_contestinvite'),(51,'Can change contest invite',18,'change_contestinvite'),(52,'Can delete contest invite',18,'delete_contestinvite'),(53,'Can add contest',19,'add_contest'),(54,'Can change contest',19,'change_contest'),(55,'Can delete contest',19,'delete_contest'),(56,'Can add alert',20,'add_alert'),(57,'Can change alert',20,'change_alert'),(58,'Can delete alert',20,'delete_alert'),(59,'Can add target',21,'add_target'),(60,'Can change target',21,'change_target'),(61,'Can delete target',21,'delete_target');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$30000$A73psQbggcOY$4UwhcGccpD8+I6sl+RHWgmFzoIxjm640hbU1rKDDn8s=','2016-10-23 17:31:19.744000',1,'admin','','','admin@virginia.edu',1,1,'2016-10-23 17:23:07.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_contest`
--

DROP TABLE IF EXISTS `contests_contest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_contest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `languages` varchar(64) NOT NULL,
  `contest_length` time(6) DEFAULT NULL,
  `contest_start` datetime(6) DEFAULT NULL,
  `time_penalty` varchar(20) DEFAULT NULL,
  `autojudge_enabled` tinyint(1) NOT NULL,
  `autojudge_review` varchar(128) DEFAULT NULL,
  `problem_description` varchar(100) DEFAULT NULL,
  `creator_id` int(11),
  PRIMARY KEY (`id`),
  KEY `contests_contest_3700153c` (`creator_id`),
  CONSTRAINT `contests_contest_creator_id_f9f17244_fk_auth_user_id` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_contest`
--

LOCK TABLES `contests_contest` WRITE;
/*!40000 ALTER TABLE `contests_contest` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_contest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_contest_contest_admins`
--

DROP TABLE IF EXISTS `contests_contest_contest_admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_contest_contest_admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contest_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `contests_contest_contest_admins_contest_id_cbe9c3c8_uniq` (`contest_id`,`user_id`),
  KEY `contests_contest_contest_admins_user_id_38c9c0ce_fk_auth_user_id` (`user_id`),
  CONSTRAINT `contests_contest_cont_contest_id_a1c926d7_fk_contests_contest_id` FOREIGN KEY (`contest_id`) REFERENCES `contests_contest` (`id`),
  CONSTRAINT `contests_contest_contest_admins_user_id_38c9c0ce_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_contest_contest_admins`
--

LOCK TABLES `contests_contest_contest_admins` WRITE;
/*!40000 ALTER TABLE `contests_contest_contest_admins` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_contest_contest_admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_contest_contest_participants`
--

DROP TABLE IF EXISTS `contests_contest_contest_participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_contest_contest_participants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contest_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `contests_contest_contest_participants_contest_id_d14a30c1_uniq` (`contest_id`,`team_id`),
  KEY `contests_contest_contest_parti_team_id_af07e09c_fk_teams_team_id` (`team_id`),
  CONSTRAINT `contests_contest_cont_contest_id_0148713b_fk_contests_contest_id` FOREIGN KEY (`contest_id`) REFERENCES `contests_contest` (`id`),
  CONSTRAINT `contests_contest_contest_parti_team_id_af07e09c_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_contest_contest_participants`
--

LOCK TABLES `contests_contest_contest_participants` WRITE;
/*!40000 ALTER TABLE `contests_contest_contest_participants` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_contest_contest_participants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_contestinvite`
--

DROP TABLE IF EXISTS `contests_contestinvite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_contestinvite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contest_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contests_contestinvite_41b6de5d` (`contest_id`),
  KEY `contests_contestinvite_f6a7ca40` (`team_id`),
  CONSTRAINT `contests_contestinvit_contest_id_00e62e70_fk_contests_contest_id` FOREIGN KEY (`contest_id`) REFERENCES `contests_contest` (`id`),
  CONSTRAINT `contests_contestinvite_team_id_aa0f42d6_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_contestinvite`
--

LOCK TABLES `contests_contestinvite` WRITE;
/*!40000 ALTER TABLE `contests_contestinvite` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_contestinvite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_contesttemplate`
--

DROP TABLE IF EXISTS `contests_contesttemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_contesttemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `languages` varchar(64) NOT NULL,
  `contest_length` time(6) DEFAULT NULL,
  `time_penalty` varchar(20) DEFAULT NULL,
  `autojudge_enabled` tinyint(1) NOT NULL,
  `autojudge_review` varchar(128) DEFAULT NULL,
  `creator_id` int(11),
  PRIMARY KEY (`id`),
  KEY `contests_contesttemplate_3700153c` (`creator_id`),
  CONSTRAINT `contests_contesttemplate_creator_id_7d42ce9a_fk_auth_user_id` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_contesttemplate`
--

LOCK TABLES `contests_contesttemplate` WRITE;
/*!40000 ALTER TABLE `contests_contesttemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_contesttemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_contesttemplate_contest_admins`
--

DROP TABLE IF EXISTS `contests_contesttemplate_contest_admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_contesttemplate_contest_admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contesttemplate_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `contests_contesttemplate_contes_contesttemplate_id_7f28f31b_uniq` (`contesttemplate_id`,`user_id`),
  KEY `contests_contesttemplate_contes_user_id_88cbdda8_fk_auth_user_id` (`user_id`),
  CONSTRAINT `conte_contesttemplate_id_2104ff67_fk_contests_contesttemplate_id` FOREIGN KEY (`contesttemplate_id`) REFERENCES `contests_contesttemplate` (`id`),
  CONSTRAINT `contests_contesttemplate_contes_user_id_88cbdda8_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_contesttemplate_contest_admins`
--

LOCK TABLES `contests_contesttemplate_contest_admins` WRITE;
/*!40000 ALTER TABLE `contests_contesttemplate_contest_admins` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_contesttemplate_contest_admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_contesttemplate_contest_participants`
--

DROP TABLE IF EXISTS `contests_contesttemplate_contest_participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_contesttemplate_contest_participants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contesttemplate_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `contests_contesttemplate_contes_contesttemplate_id_e1e23b12_uniq` (`contesttemplate_id`,`team_id`),
  KEY `contests_contesttemplate_conte_team_id_f6b5f6cd_fk_teams_team_id` (`team_id`),
  CONSTRAINT `conte_contesttemplate_id_0bb33390_fk_contests_contesttemplate_id` FOREIGN KEY (`contesttemplate_id`) REFERENCES `contests_contesttemplate` (`id`),
  CONSTRAINT `contests_contesttemplate_conte_team_id_f6b5f6cd_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_contesttemplate_contest_participants`
--

LOCK TABLES `contests_contesttemplate_contest_participants` WRITE;
/*!40000 ALTER TABLE `contests_contesttemplate_contest_participants` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_contesttemplate_contest_participants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_notification`
--

DROP TABLE IF EXISTS `contests_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `submission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contests_notification_1dd9cfcc` (`submission_id`),
  CONSTRAINT `contests_no_submission_id_170aae40_fk_contests_submission_run_id` FOREIGN KEY (`submission_id`) REFERENCES `contests_submission` (`run_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_notification`
--

LOCK TABLES `contests_notification` WRITE;
/*!40000 ALTER TABLE `contests_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_participant`
--

DROP TABLE IF EXISTS `contests_participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_participant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contest_id` int(11),
  `team_id` int(11),
  PRIMARY KEY (`id`),
  KEY `contests_participant_41b6de5d` (`contest_id`),
  KEY `contests_participant_f6a7ca40` (`team_id`),
  CONSTRAINT `contests_participant_contest_id_d1dd1e82_fk_contests_contest_id` FOREIGN KEY (`contest_id`) REFERENCES `contests_contest` (`id`),
  CONSTRAINT `contests_participant_team_id_a51351ce_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_participant`
--

LOCK TABLES `contests_participant` WRITE;
/*!40000 ALTER TABLE `contests_participant` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_problem`
--

DROP TABLE IF EXISTS `contests_problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_problem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(2048) DEFAULT NULL,
  `input_description` longtext,
  `output_description` longtext,
  `sample_input` varchar(100) DEFAULT NULL,
  `sample_output` varchar(100) DEFAULT NULL,
  `solution` varchar(100) DEFAULT NULL,
  `timeout` int(11) NOT NULL,
  `contest_id` int(11),
  PRIMARY KEY (`id`),
  KEY `contests_problem_41b6de5d` (`contest_id`),
  CONSTRAINT `contests_problem_contest_id_cbf51a2c_fk_contests_contest_id` FOREIGN KEY (`contest_id`) REFERENCES `contests_contest` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_problem`
--

LOCK TABLES `contests_problem` WRITE;
/*!40000 ALTER TABLE `contests_problem` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_problem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_probleminput`
--

DROP TABLE IF EXISTS `contests_probleminput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_probleminput` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_input` varchar(100) DEFAULT NULL,
  `problem_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contests_probleminput_919b1d80` (`problem_id`),
  CONSTRAINT `contests_probleminput_problem_id_4d60c847_fk_contests_problem_id` FOREIGN KEY (`problem_id`) REFERENCES `contests_problem` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_probleminput`
--

LOCK TABLES `contests_probleminput` WRITE;
/*!40000 ALTER TABLE `contests_probleminput` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_probleminput` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contests_submission`
--

DROP TABLE IF EXISTS `contests_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contests_submission` (
  `run_id` int(11) NOT NULL AUTO_INCREMENT,
  `code_file` varchar(100) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `original_filename` varchar(128) DEFAULT NULL,
  `state` varchar(20) NOT NULL,
  `result` varchar(20) DEFAULT NULL,
  `problem_id` int(11) DEFAULT NULL,
  `team_id` int(11),
  PRIMARY KEY (`run_id`),
  KEY `contests_submission_problem_id_a337e212_fk_contests_problem_id` (`problem_id`),
  KEY `contests_submission_f6a7ca40` (`team_id`),
  CONSTRAINT `contests_submission_problem_id_a337e212_fk_contests_problem_id` FOREIGN KEY (`problem_id`) REFERENCES `contests_problem` (`id`),
  CONSTRAINT `contests_submission_team_id_499eaefc_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contests_submission`
--

LOCK TABLES `contests_submission` WRITE;
/*!40000 ALTER TABLE `contests_submission` DISABLE KEYS */;
/*!40000 ALTER TABLE `contests_submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (4,'admin','logentry'),(20,'alerts','alert'),(21,'alerts','target'),(2,'auth','group'),(3,'auth','permission'),(1,'auth','user'),(5,'contenttypes','contenttype'),(19,'contests','contest'),(18,'contests','contestinvite'),(17,'contests','contesttemplate'),(12,'contests','notification'),(14,'contests','participant'),(15,'contests','problem'),(16,'contests','probleminput'),(13,'contests','submission'),(6,'sessions','session'),(10,'teams','invite'),(11,'teams','joinrequest'),(9,'teams','team'),(8,'users','user'),(7,'users','userprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-04-28 01:33:33.114433'),(2,'auth','0001_initial','2017-04-28 01:33:33.683619'),(3,'admin','0001_initial','2017-04-28 01:33:33.849596'),(4,'admin','0002_logentry_remove_auto_add','2017-04-28 01:33:33.876434'),(5,'contenttypes','0002_remove_content_type_name','2017-04-28 01:33:33.976805'),(6,'auth','0002_alter_permission_name_max_length','2017-04-28 01:33:34.000641'),(7,'auth','0003_alter_user_email_max_length','2017-04-28 01:33:34.029524'),(8,'auth','0004_alter_user_username_opts','2017-04-28 01:33:34.042511'),(9,'auth','0005_alter_user_last_login_null','2017-04-28 01:33:34.085649'),(10,'auth','0006_require_contenttypes_0002','2017-04-28 01:33:34.091711'),(11,'auth','0007_alter_validators_add_error_messages','2017-04-28 01:33:34.107430'),(12,'auth','0008_alter_user_username_max_length','2017-04-28 01:33:34.145435'),(13,'users','0001_initial','2017-04-28 01:33:34.269892'),(14,'teams','0001_initial','2017-04-28 01:33:34.355578'),(15,'contests','0001_initial','2017-04-28 01:33:34.630533'),(16,'alerts','0001_initial','2017-04-28 01:33:34.690674'),(17,'alerts','0002_target_contest','2017-04-28 01:33:35.112439'),(18,'alerts','0003_auto_20170328_0137','2017-04-28 01:33:35.474807'),(19,'alerts','0004_auto_20170328_0137','2017-04-28 01:33:35.866241'),(20,'contests','0002_auto_20170328_0137','2017-04-28 01:33:36.469572'),(21,'contests','0003_auto_20170328_0137','2017-04-28 01:33:37.646422'),(22,'contests','0004_auto_20170401_1457','2017-04-28 01:33:37.801094'),(23,'contests','0005_auto_20170401_1809','2017-04-28 01:33:38.080121'),(24,'contests','0006_auto_20170408_1719','2017-04-28 01:33:38.296988'),(25,'contests','0007_auto_20170412_1419','2017-04-28 01:33:38.478751'),(26,'contests','0005_auto_20170409_2224','2017-04-28 01:33:38.687579'),(27,'contests','0006_merge_20170410_1013','2017-04-28 01:33:38.693188'),(28,'contests','0008_merge_20170422_1359','2017-04-28 01:33:38.696817'),(29,'contests','0009_auto_20170422_1411','2017-04-28 01:33:38.900329'),(30,'contests','0010_auto_20170423_2046','2017-04-28 01:33:38.988358'),(31,'contests','0011_auto_20170423_2052','2017-04-28 01:33:39.151125'),(32,'contests','0012_auto_20170425_1102','2017-04-28 01:33:39.380591'),(33,'sessions','0001_initial','2017-04-28 01:33:39.430167'),(34,'teams','0002_auto_20170328_0137','2017-04-28 01:33:40.217709');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams_invite`
--

DROP TABLE IF EXISTS `teams_invite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams_invite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `team_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teams_invite_f6a7ca40` (`team_id`),
  KEY `teams_invite_e8701ad4` (`user_id`),
  CONSTRAINT `teams_invite_team_id_2c8f31a2_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`),
  CONSTRAINT `teams_invite_user_id_e2df9f83_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams_invite`
--

LOCK TABLES `teams_invite` WRITE;
/*!40000 ALTER TABLE `teams_invite` DISABLE KEYS */;
/*!40000 ALTER TABLE `teams_invite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams_joinrequest`
--

DROP TABLE IF EXISTS `teams_joinrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams_joinrequest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `team_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teams_joinrequest_f6a7ca40` (`team_id`),
  KEY `teams_joinrequest_e8701ad4` (`user_id`),
  CONSTRAINT `teams_joinrequest_team_id_d5688fb0_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`),
  CONSTRAINT `teams_joinrequest_user_id_e68499ef_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams_joinrequest`
--

LOCK TABLES `teams_joinrequest` WRITE;
/*!40000 ALTER TABLE `teams_joinrequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `teams_joinrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams_team`
--

DROP TABLE IF EXISTS `teams_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams_team` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `public` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams_team`
--

LOCK TABLES `teams_team` WRITE;
/*!40000 ALTER TABLE `teams_team` DISABLE KEYS */;
/*!40000 ALTER TABLE `teams_team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams_team_members`
--

DROP TABLE IF EXISTS `teams_team_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams_team_members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `teams_team_members_team_id_7b6a61ef_uniq` (`team_id`,`user_id`),
  KEY `teams_team_members_user_id_d2b52fb4_fk_auth_user_id` (`user_id`),
  CONSTRAINT `teams_team_members_team_id_ebb2d47d_fk_teams_team_id` FOREIGN KEY (`team_id`) REFERENCES `teams_team` (`id`),
  CONSTRAINT `teams_team_members_user_id_d2b52fb4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams_team_members`
--

LOCK TABLES `teams_team_members` WRITE;
/*!40000 ALTER TABLE `teams_team_members` DISABLE KEYS */;
/*!40000 ALTER TABLE `teams_team_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_userprofile`
--

DROP TABLE IF EXISTS `users_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `theme` varchar(200) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `users_userprofile_user_id_87251ef1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_userprofile`
--

LOCK TABLES `users_userprofile` WRITE;
/*!40000 ALTER TABLE `users_userprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_userprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-28  1:34:28
