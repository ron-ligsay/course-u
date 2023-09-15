-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: courseu_db
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add specialization',7,'add_specialization'),(26,'Can change specialization',7,'change_specialization'),(27,'Can delete specialization',7,'delete_specialization'),(28,'Can view specialization',7,'view_specialization'),(29,'Can add test',8,'add_test'),(30,'Can change test',8,'change_test'),(31,'Can delete test',8,'delete_test'),(32,'Can view test',8,'view_test');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$4fJXyK07PYn2iqIU57TNXF$XdGohwySWljfZ1jm+gprjNahM+35NH1iCUKLmGg0rPo=','2023-08-28 11:16:53.376647',1,'admin','','','admin@gmail.com',1,1,'2023-08-26 17:39:05.486083'),(2,'pbkdf2_sha256$600000$JDpUoL0EotSOD9Emad9c6o$qf0aoLKb6gJieM31wHUrGAwL/noVaHzndDc5waRQgSM=','2023-08-27 07:43:05.602682',1,'aky','','','aky@gmail.com',1,1,'2023-08-27 02:46:28.534069'),(3,'pbkdf2_sha256$600000$9fwutkTGhFIHukfRdVqH1O$j23T5VASeh3SB7sds0/rAxl3+7n/IMNNt2Wa7tXkWso=','2023-08-27 08:17:21.336700',0,'charlotte','Charlotte','Balbido','charlotte@gmail.com',0,1,'2023-08-27 08:17:20.117203');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'website','specialization'),(8,'website','test');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-08-26 17:32:25.075849'),(2,'auth','0001_initial','2023-08-26 17:32:25.792837'),(3,'admin','0001_initial','2023-08-26 17:32:26.032881'),(4,'admin','0002_logentry_remove_auto_add','2023-08-26 17:32:26.048455'),(5,'admin','0003_logentry_add_action_flag_choices','2023-08-26 17:32:26.064082'),(6,'contenttypes','0002_remove_content_type_name','2023-08-26 17:32:26.189184'),(7,'auth','0002_alter_permission_name_max_length','2023-08-26 17:32:26.251582'),(8,'auth','0003_alter_user_email_max_length','2023-08-26 17:32:26.298462'),(9,'auth','0004_alter_user_username_opts','2023-08-26 17:32:26.314082'),(10,'auth','0005_alter_user_last_login_null','2023-08-26 17:32:26.376581'),(11,'auth','0006_require_contenttypes_0002','2023-08-26 17:32:26.376581'),(12,'auth','0007_alter_validators_add_error_messages','2023-08-26 17:32:26.392290'),(13,'auth','0008_alter_user_username_max_length','2023-08-26 17:32:26.470345'),(14,'auth','0009_alter_user_last_name_max_length','2023-08-26 17:32:26.532839'),(15,'auth','0010_alter_group_name_max_length','2023-08-26 17:32:26.564150'),(16,'auth','0011_update_proxy_permissions','2023-08-26 17:32:26.595331'),(17,'auth','0012_alter_user_first_name_max_length','2023-08-26 17:32:26.657828'),(18,'sessions','0001_initial','2023-08-26 17:32:26.720434'),(19,'website','0001_initial','2023-08-28 08:04:30.561301'),(20,'website','0002_rename_option_1_test_option1_and_more','2023-08-28 08:05:16.401326'),(21,'website','0003_initial','2023-08-28 11:11:54.680645');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `website_specialization`
--

DROP TABLE IF EXISTS `website_specialization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `website_specialization` (
  `specialization_id` int NOT NULL AUTO_INCREMENT,
  `field_id` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `roadmap_id` int NOT NULL,
  PRIMARY KEY (`specialization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `website_specialization`
--

LOCK TABLES `website_specialization` WRITE;
/*!40000 ALTER TABLE `website_specialization` DISABLE KEYS */;
INSERT INTO `website_specialization` VALUES (1,'Software Development','front-end','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',1),(2,'Software Development','back-end','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',2),(3,'Software Development','full stack','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',3),(4,'Software Development','software engineer','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',4),(5,'Software Development','software developer','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',5),(6,'Software Development','mobile app developer','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',6),(7,'Software Development','devops engineer','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',7),(8,'Software Development','game developer','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',8),(9,'Software Development','embedded systems developer','Developer roles, including front-end, back-end, full stack, and specialized roles like game and mobile app developers.',9),(10,'Data and Analytics','data scientist','Roles focused on data analysis, including data scientists, analysts, and engineers working on machine learning and AI.',10),(11,'Data and Analytics','data analyst','Roles focused on data analysis, including data scientists, analysts, and engineers working on machine learning and AI.',11),(12,'Data and Analytics','business intelligence (BI) developer','Roles focused on data analysis, including data scientists, analysts, and engineers working on machine learning and AI.',12),(13,'Data and Analytics','machine learning engineer','Roles focused on data analysis, including data scientists, analysts, and engineers working on machine learning and AI.',13),(14,'Data and Analytics','ai engineer','Roles focused on data analysis, including data scientists, analysts, and engineers working on machine learning and AI.',14),(15,'Data and Analytics','data engineer','Roles focused on data analysis, including data scientists, analysts, and engineers working on machine learning and AI.',15),(16,'Design and UX/UI','UI Designer','Roles involved in designing user interfaces and creating optimal user experiences.',16),(17,'Design and UX/UI','UX Designer','Roles involved in designing user interfaces and creating optimal user experiences.',17),(18,'Design and UX/UI','Interaction Designer','Roles involved in designing user interfaces and creating optimal user experiences.',18),(19,'Design and UX/UI','Visual Designer','Roles involved in designing user interfaces and creating optimal user experiences.',19),(20,'Product Management','product manager','Roles overseeing product development, strategy, and roadmap.',20),(21,'Product Management','technical product manager','Roles overseeing product development, strategy, and roadmap.',21),(22,'Testing and Quality Assurance','qa engineer','Roles responsible for ensuring software quality through testing.',22),(23,'Testing and Quality Assurance','test automation engineer','Roles responsible for ensuring software quality through testing.',23),(24,'Security','cybersecurity analyst','Roles centered around cybersecurity and protecting systems and data.',24),(25,'Security','security engineer','Roles centered around cybersecurity and protecting systems and data.',25),(26,'Security','ethical hacker (penetration tester)','Roles centered around cybersecurity and protecting systems and data.',26),(27,'Security','security consultant','Roles centered around cybersecurity and protecting systems and data.',27),(28,'Networking and Infrastructure','network engineer','Roles managing networks, systems, and cloud infrastructure.',28),(29,'Networking and Infrastructure','system administrator','Roles managing networks, systems, and cloud infrastructure.',29),(30,'Networking and Infrastructure','cloud engineer','Roles managing networks, systems, and cloud infrastructure.',30),(31,'Networking and Infrastructure','site reliability engineer (se)','Roles managing networks, systems, and cloud infrastructure.',31),(32,'Project Management','it project mananger','Roles providing technical assistance to end-users.',32),(33,'Project Management','scrum master','Roles providing technical assistance to end-users.',33),(34,'Business and Strategy','it business analyst','Roles leading and managing IT projects.',34),(35,'Business and Strategy','it consultant','Roles leading and managing IT projects.',35),(36,'Business and Strategy','technology strategist','Roles leading and managing IT projects.',36),(37,'Emerging and Specialized','blockchain developer','Roles in cutting-edge technologies and areas like blockchain, VR, and quantum computing.',37),(38,'Emerging and Specialized','quantum computing scientist','Roles in cutting-edge technologies and areas like blockchain, VR, and quantum computing.',38),(39,'Emerging and Specialized','virtual reality (vr) developer','Roles in cutting-edge technologies and areas like blockchain, VR, and quantum computing.',39),(40,'Emerging and Specialized','augmented reality (ar) developer','Roles in cutting-edge technologies and areas like blockchain, VR, and quantum computing.',40),(41,'Emerging and Specialized','edge computing engineer','Roles in cutting-edge technologies and areas like blockchain, VR, and quantum computing.',41);
/*!40000 ALTER TABLE `website_specialization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `website_test`
--

DROP TABLE IF EXISTS `website_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `website_test` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `question` varchar(1000) NOT NULL,
  `option1` varchar(1000) NOT NULL,
  `option2` varchar(1000) NOT NULL,
  `option3` varchar(1000) NOT NULL,
  `option4` varchar(1000) NOT NULL,
  `answer` varchar(1000) NOT NULL,
  `topic` varchar(1000) NOT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `website_test`
--

LOCK TABLES `website_test` WRITE;
/*!40000 ALTER TABLE `website_test` DISABLE KEYS */;
INSERT INTO `website_test` VALUES (1,'What is python?','ahas','snake','conda','all of the above','option 2','Personality'),(2,'What is HTML?','hot talong mayonaise latte','how to make lumpia','hyper text markup language','suko na ko','option 4','Personality'),(3,'What is Art?','si crush1','art','tanong mo kay sir','art is art','option 3','Personality'),(4,'Hotdog','option 1','option 2','option 3','option 4','option 2','Personality'),(5,'Question 5','option 1','option 2','option 3','option 4','option 3','Personality'),(6,'Question 6','option 1','option 2','option 3','option 4','option 3','Personality'),(7,'Question 7','option 1','option 2','option 3','option 4','option 1','Personality'),(8,'Question 8','option 1','option 2','option 3','option 4','option 2','Personality'),(9,'Question 9','option 1','option 2','option 3','option 4','option 2','Personality'),(10,'Question 10','option 1','option 2','option 3','option 4','option 1','Personality'),(11,'Question 11','option 1','option 2','option 3','option 4','option 1','Personality'),(12,'Question 12','option 1','option 2','option 3','option 4','option 2','Personality'),(13,'Question 13','option 1','option 2','option 3','option 4','option 4','Personality'),(14,'Question 14','option 1','option 2','option 3','option 4','option 3','Personality'),(15,'Question 15','option 1','option 2','option 3','option 4','option 1','Personality'),(16,'Question 16','option 1','option 2','option 3','option 4','option 1','Personality'),(17,'Question 17','option 1','option 2','option 3','option 4','option 4','Personality'),(18,'Question 18','option 1','option 2','option 3','option 4','option 4','Personality'),(19,'Question 19','option 1','option 2','option 3','option 4','option 2','Personality'),(20,'Question 20','option 1','option 2','option 3','option 4','option 3','Personality'),(21,'Question 21','option 1','option 2','option 3','option 4','option 3','Personality'),(22,'Question 22','option 1','option 2','option 3','option 4','option 4','Personality');
/*!40000 ALTER TABLE `website_test` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-07 18:23:47
