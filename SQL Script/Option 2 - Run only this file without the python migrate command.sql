-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: beautynailnet
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Create database
--

CREATE DATABASE IF NOT EXISTS beautynailnet;
USE beautynailnet;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `appointment_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time DEFAULT NULL,
  `status` varchar(20) DEFAULT 'scheduled',
  `total_amount` decimal(8,2) DEFAULT NULL,
  `notes` text,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appointment_id`),
  KEY `customer_id` (`customer_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1017 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (11,11,1,'2024-07-22','09:00:00','10:00:00','scheduled',45.00,'First-time client','2025-07-19 10:52:28'),(12,12,3,'2024-07-22','10:30:00','11:30:00','completed',35.00,'Regular customer','2025-07-19 10:52:28'),(13,13,2,'2024-07-23','14:00:00','15:00:00','scheduled',60.00,'Spa pedicure','2025-07-19 10:52:28'),(14,14,1,'2024-07-23','15:30:00','16:30:00','completed',25.00,'Quick polish change','2025-07-19 10:52:28'),(15,15,4,'2024-07-24','11:00:00','12:30:00','scheduled',55.00,'Acrylic full set','2025-07-19 10:52:28'),(16,16,2,'2024-07-24','09:00:00','09:30:00','completed',25.00,'French manicure','2025-07-19 10:52:28'),(17,17,3,'2024-07-25','09:30:00','10:30:00','scheduled',40.00,'Classic pedicure','2025-07-19 10:52:28'),(18,18,1,'2024-07-25','14:30:00','15:30:00','completed',35.00,'Gel manicure','2025-07-19 10:52:28'),(19,19,5,'2024-07-26','10:00:00','11:00:00','scheduled',25.00,'Classic manicure','2025-07-19 10:52:28'),(20,20,2,'2024-07-26','10:30:00','12:00:00','scheduled',30.00,'Nail art designdgsg','2025-07-19 10:52:28'),(1000,19,7,'2025-08-13','09:00:00','10:30:00','scheduled',32.00,'dasfddsfdafdfasf','2025-08-14 12:24:55'),(1001,11,10,'2025-08-13','15:00:00','16:30:00','pending',25.00,'daf','2025-08-14 12:27:35'),(1011,11,8,'2025-08-22','10:30:00','10:55:00','completed',20.00,'good','2025-08-21 02:25:11'),(1015,1009,2,'2025-08-21','10:30:00','10:55:00','pending',20.00,'note','2025-08-22 13:30:59'),(1016,1010,3,'2025-08-03','18:30:00','18:55:00','pending',20.00,'r','2025-08-23 01:38:43');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointment_service`
--

DROP TABLE IF EXISTS `appointment_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment_service` (
  `appointment_service_id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `service_id` int NOT NULL,
  `service_price` decimal(8,2) NOT NULL,
  `polish_color` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`appointment_service_id`),
  KEY `appointment_id` (`appointment_id`),
  KEY `service_id` (`service_id`),
  CONSTRAINT `appointment_service_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`appointment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `appointment_service_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment_service`
--

LOCK TABLES `appointment_service` WRITE;
/*!40000 ALTER TABLE `appointment_service` DISABLE KEYS */;
INSERT INTO `appointment_service` VALUES (13,11,1,25.00,'Classic Red'),(14,11,7,20.00,'Gold accent'),(15,12,2,35.00,'Pink Shimmer'),(16,13,6,60.00,'French White'),(17,14,9,15.00,'Clear'),(18,15,4,55.00,'Nude Pink'),(20,17,5,40.00,'Ocean Blue'),(21,18,2,35.00,'Gel Red'),(22,19,1,25.00,'Classic Pink'),(33,1001,3,25.00,'dfa'),(34,20,7,30.00,'Silver glitter'),(42,1000,2,20.00,'sf'),(43,1000,4,12.00,'dfs'),(44,16,3,25.00,'French White'),(76,1011,2,20.00,'red'),(83,1015,2,20.00,'red'),(84,1016,2,20.00,'red');
/*!40000 ALTER TABLE `appointment_service` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session');
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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$RiWhm3agStyCcbeEGx0h3X$xaDhoqmdHSTO+vCIjUbNLjhIPZaIeKwTu6DI5v/atXA=','2025-08-22 18:54:00.652152',1,'admin','admin','staff','admin@gmail.com',1,1,'2025-08-13 22:21:19.000000'),(2,'pbkdf2_sha256$1000000$Fn0RZNRxwR9BLjcTNEaQqg$vOYXITcbC2NXneAhSk8vXV7F3tQ+SoeJ8w8RkaTyXbQ=','2025-08-22 06:39:16.557593',0,'user1','Todd','Sims','todd.sims@email.com',0,1,'2025-08-13 22:21:19.000000'),(3,'pbkdf2_sha256$1000000$Vf5uTFBUG9nxzdATuvav0X$wzzEv5e6LswUo7VmNEhnV8rVAju41K5+iDHdVbMqTkw=',NULL,0,'user2','Robin','Harris','robin.harris@yahoo.com',0,1,'2025-08-13 22:21:19.000000'),(4,'pbkdf2_sha256$1000000$4V1koRe2V5qSyzsU1fbwGb$j3BWDqDbobiWhiEvpX69SzeVRplCeQn2oHaIxZSXGhs=',NULL,0,'user3','Nancy','Deleon','nancy.deleon@hotmail.com',0,1,'2025-08-13 22:21:19.000000'),(5,'pbkdf2_sha256$1000000$RZhoi9d7lRqMbfkukNWOdc$AVjmRndXuPuVsYw3UteT8l+OZgOnQMngafQVR+JcNrE=',NULL,0,'user4','Raymond','Miller','raymond.miller@email.com',0,1,'2025-08-13 22:21:19.000000'),(6,'pbkdf2_sha256$1000000$vgpf7yLkYpi43BGGaU4HKU$VxmhyCdN4mm/0DSKUOmO67irkY6lXMx9X8U3LkVSG0M=',NULL,0,'user5','Alyssa','Jackson','alyssa.jackson@gmail.com',0,1,'2025-08-13 22:21:19.000000'),(7,'pbkdf2_sha256$1000000$tR52LxJ845Py2ZwGDZnqCZ$kzpchf+tULmaUaN8gB5k9qTBa70mecd1BMdYKn5mXrI=',NULL,0,'user6','Hailey','Webb','hailey.webb@hotmail.com',0,1,'2025-08-13 22:21:19.000000'),(8,'pbkdf2_sha256$1000000$YJmd2XXGv9hQKFvhn6xlBq$oHUkbF54rnv1uSTtvWjhFb68I9kJVAQCsShtp84c2PE=',NULL,0,'user7','Jessica','Irwin','jessica.irwin@email.com',0,1,'2025-08-13 22:21:19.000000'),(9,'pbkdf2_sha256$1000000$aGRWKyw6JwCHR8wEswoFDh$Tx+Cvuj0XdlI6wUV8qwbEmPPmNEl3RjbY7P9QxcNgaE=',NULL,0,'user8','Tina','Rhodes','tina.rhodes@email.com',0,1,'2025-08-13 22:21:19.000000'),(10,'pbkdf2_sha256$1000000$HR54YSziabH3tSwIALMsFH$9WaBzwX2pjeov8NgoY/F2aUWMVaKnFdTx6iIsQq2srs=',NULL,0,'user9','Anne','Johnson','anne.johnson@hotmail.com',0,1,'2025-08-13 22:21:19.000000'),(11,'pbkdf2_sha256$1000000$Vmp6ivWTXOVhaiy6SOnk3q$JaFxHuTe7gRXgtCGRbtpp2Jn6271Lm2Ueqs+ZnvuhWo=',NULL,0,'user10','Rachel','Wheeler','rachel.wheeler@email.com',0,1,'2025-08-13 22:21:19.000000'),(12,'pbkdf2_sha256$1000000$wTZVezsuO0RrgnpMJLSMzU$0oVu8heEh/TBRekdsvVCmQjQIAtQ6NeC0c9scWAeyYU=','2025-08-22 06:13:31.842052',0,'staff1','Linda','Miao','linda.miao@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(13,'pbkdf2_sha256$1000000$OMsPvUK6vDNX3SeCeszRkH$i4WInc4zxkVKtC6+0BUXXnyVsuGgmr7n1aB/GS5FKmE=','2025-08-22 06:14:25.211960',0,'staff2','Emily','Rodriguez','emily.rodriguez@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(14,'pbkdf2_sha256$1000000$cVVPD2VoWNx0Yd68m3X6LG$k3QrpthUfqHA616ShcW05IPtnV9CFqxB1aMiItRWahU=',NULL,0,'staff3','Jessica','Chen','jessica.chen@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(15,'pbkdf2_sha256$1000000$O19ZKASjbdyMq2r8PiH0i6$EKPhfuQODA1gGCH46zzAYtRFZ8fHhmfotIxN27QT/QM=',NULL,0,'staff4','Sophia','Kim','sophia.kim@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(16,'pbkdf2_sha256$1000000$5pA2hjgqwRC7ZeZIxwNnxL$I+o8MU8MlpLDQlGuwrpJEj+TnFFz060/8mN6jor4J7I=','2025-08-20 20:21:37.271911',0,'staff5','Madison','Thompson','madison.thompson@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(17,'pbkdf2_sha256$1000000$dJGUf4ABqNU9HF7xTa2dvx$q1/woZ1s27N8nO+nMsZypf9Z4Zx/dgfQ7kRp1b++AIo=',NULL,0,'staff6','Ashley','Garcia','ashley.garcia@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(18,'pbkdf2_sha256$1000000$xn7U9XQu571JHtsnQ1eTu8$BzWL2/Ewkeey79GyC2+FzxSUKISfD0MRBHv31q64zX8=',NULL,0,'staff7','Taylor','White','taylor.white@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(19,'pbkdf2_sha256$1000000$qjwiLEu7awHvmg65OrMqnF$fDrMFk0l5C5PZGafpwPpRAPggmRQT4WaxH/XkaOk99Y=',NULL,0,'staff8','Olivia','Martinez','olivia.martinez@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(20,'pbkdf2_sha256$1000000$kPGElMtBShBGCwwI6Db5L7$kXaWqY9pIwmcqooMeQFL/GWkwGH9nNMSmwQBPXbO8vE=','2025-08-19 20:46:54.871256',0,'staff9','Hannah','Lee','hannah.lee@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(21,'pbkdf2_sha256$1000000$Rpt5ULYBJIYnUQXa5mQiAj$XJJQjaP9zJz7P3OmfYPnV029/5b56Cxk4g+EHB0bfNY=',NULL,0,'staff10','Megan','Jackson','megan.jackson@beautynailnet.com',1,1,'2025-08-16 03:54:30.000000'),(22,'pbkdf2_sha256$1000000$QkVecw6dzGLWsrqGTfglCZ$PmFu762NsQ5FEFN8L0dJ+s0pG5YYr6WaZGx6W3GUpZc=',NULL,0,'t','t','t','t@gmail.com',0,1,'2025-08-16 12:12:01.115942'),(23,'pbkdf2_sha256$1000000$HudQ9vABlJTjE2ewcazf3S$b2wOxKERZN0p6BSmFnHb/WyZBBeFCCVBgsbmNqQwKOQ=','2025-08-19 20:45:44.642524',0,'f@gmail.com','f','f','f@gmail.com',0,1,'2025-08-19 20:43:15.537593'),(24,'pbkdf2_sha256$1000000$QyrlDSDgFeu6DubDaeKX0V$dv31oCvCCmxmDCOOoX/4OQeTyv/gnIIfoMwDsFM8DpI=','2025-08-19 23:29:43.580835',0,'myhhs@outlook.com','Linda','Miao','myhhs@outlook.com',0,1,'2025-08-19 23:15:21.791455'),(25,'pbkdf2_sha256$1000000$KYqhQddDFkg4PXcidvJ4ow$DKmUN3CcH8VdQHzZ2qWtWpvlFodvliImEI1lZOPQKFw=','2025-08-20 00:16:01.796979',0,'l@gmail.com','Linda','Miao','l@gmail.com',0,1,'2025-08-20 00:10:15.614847'),(26,'pbkdf2_sha256$1000000$YQMWy52VT4dQQEwLSQ8t3j$Pb4chqt9K5CPBfVWNgFXxH7HrIJa3cGZDV6VFpm8zwg=','2025-08-22 06:31:24.591844',0,'ym@gmail.com','y','m','ym@gmail.com',0,1,'2025-08-20 00:33:44.500629'),(27,'pbkdf2_sha256$1000000$s6OiLuNmc84nR0MisRfD4C$ltlsXLtGQcy6PF+4i+qJ56N8b35+q7ssAbIVgqEQbuY=','2025-08-22 18:39:01.128543',0,'gm@gmail.com','g','gm@gmail.com','gm@gmail.com',0,1,'2025-08-22 18:38:42.425329');
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
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `allergies` text,
  `preferred_color` varchar(50) DEFAULT NULL,
  `loyalty_points` int DEFAULT '0',
  `registration_date` date DEFAULT (curdate()),
  `is_active` tinyint(1) DEFAULT '1',
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_customer_user_id` (`user_id`),
  CONSTRAINT `fk_customer_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1011 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (11,'Todd','Sims','618-845-8073','todd.sims@email.com','1996-10-11',NULL,'Purple',100317,'2024-12-31',1,2),(12,'Robin','Harris','905-579-7081','robin.harris@yahoo.com','2000-01-19','Pollen','Red',86,'2023-01-19',1,3),(13,'Nancy','Deleon','227-854-9780','nancy.deleon@hotmail.com','1959-10-27','Pollen',NULL,289,'2023-11-09',1,4),(14,'Raymond','Miller','468-626-2871','raymond.miller@email.com','1960-01-15','Fragrance','Red',120,'2023-10-07',1,5),(15,'Alyssa','Jackson','403-441-6240','alyssa.jackson@gmail.com','1998-10-31','Dust','Pink',284,'2025-06-10',1,6),(16,'Hailey','Webb','906-416-5220','hailey.webb@hotmail.com','1965-06-06','Pollen','Red',10,'2024-01-28',0,7),(17,'Jessica','Irwin','731-049-6021','jessica.irwin@email.com','1967-12-17',NULL,'Red',16,'2022-09-07',1,8),(18,'Tina','Rhodes','037-456-5659','tina.rhodes@email.com','1961-10-10','Pollen','Green',144,'2024-01-07',1,9),(19,'Anne','Johnson','866-823-7190','anne.johnson@hotmail.com','1981-04-27','Nail polish remover','Pink',149,'2024-12-09',1,10),(20,'Rachel','Wheeler','407-484-5977','rachel.wheeler@email.com','1995-03-19',NULL,'Red',124,'2023-03-12',0,11),(1009,'y','m','12','ym@gmail.com',NULL,NULL,NULL,0,NULL,1,26),(1010,'g','gm@gmail.com','12','gm@gmail.com',NULL,NULL,NULL,0,NULL,1,27);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-08-14 05:20:30.729227'),(2,'auth','0001_initial','2025-08-14 05:20:31.621658'),(3,'admin','0001_initial','2025-08-14 05:20:31.818361'),(4,'admin','0002_logentry_remove_auto_add','2025-08-14 05:20:31.827161'),(5,'admin','0003_logentry_add_action_flag_choices','2025-08-14 05:20:31.835556'),(6,'contenttypes','0002_remove_content_type_name','2025-08-14 05:20:31.971391'),(7,'auth','0002_alter_permission_name_max_length','2025-08-14 05:20:32.068976'),(8,'auth','0003_alter_user_email_max_length','2025-08-14 05:20:32.098636'),(9,'auth','0004_alter_user_username_opts','2025-08-14 05:20:32.106300'),(10,'auth','0005_alter_user_last_login_null','2025-08-14 05:20:32.175099'),(11,'auth','0006_require_contenttypes_0002','2025-08-14 05:20:32.179150'),(12,'auth','0007_alter_validators_add_error_messages','2025-08-14 05:20:32.186419'),(13,'auth','0008_alter_user_username_max_length','2025-08-14 05:20:32.280545'),(14,'auth','0009_alter_user_last_name_max_length','2025-08-14 05:20:32.373897'),(15,'auth','0010_alter_group_name_max_length','2025-08-14 05:20:32.397974'),(16,'auth','0011_update_proxy_permissions','2025-08-14 05:20:32.406355'),(17,'auth','0012_alter_user_first_name_max_length','2025-08-14 05:20:32.502148'),(18,'sessions','0001_initial','2025-08-14 05:20:32.554993');
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
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `events_id` int NOT NULL AUTO_INCREMENT,
  `event_name` varchar(100) NOT NULL,
  `description` text,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`events_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,'Spring Blossom Special','Celebrate spring with 15% off all floral nail art designs.','2025-03-20','2025-04-30','images/events/spring_blossom.jpg'),(2,'Mother\'s Day Pamper','Treat your mom to a deluxe manicure and pedicure combo with a free gift.','2025-05-01','2025-05-12','images/events/mothers_day.jpg'),(3,'Summer Glow Up','Discounts on paraffin treatments and gel manicures to prep for summer.','2025-06-01','2025-06-30','images/events/summer_glow.jpg'),(4,'July 4th Nail Fest','Red, white, and blue nail art specials for Independence Day!','2025-07-01','2025-07-07','images/events/july4th.jpg'),(5,'Back to School Deals','Students get 20% off all basic manicures and pedicures.','2025-08-15','2025-09-15','images/events/back_to_school.jpg'),(6,'Autumn Colors Collection','Showcase of seasonal colors and limited edition polishes.','2025-09-21','2025-10-31','images/events/autumn_colors.jpg'),(7,'Halloween Nail Art Contest','Win prizes for the spookiest nail designs! Submit photos by Oct 28.','2025-10-01','2025-10-31','images/events/halloween.jpg'),(8,'Thankful Hands','Book any treatment in November and get a free cuticle oil sample.','2025-11-01','2025-11-30','images/events/thanksgiving.jpg'),(9,'Holiday Sparkle Week','Festive glitter styles and gift card giveaways all December long.','2025-12-01','2025-12-24','images/events/holiday_sparkle.jpg'),(10,'New Year, New Nails','Kick off 2026 with 10% off your first appointment of the year.','2026-01-01','2026-01-15','images/events/new_year.jpg');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `inventory_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `category` varchar(50) NOT NULL,
  `color_name` varchar(50) DEFAULT NULL,
  `quantity_in_stock` int DEFAULT '0',
  `unit_cost` decimal(6,2) NOT NULL,
  `retail_price` decimal(6,2) DEFAULT NULL,
  `reorder_level` int DEFAULT '5',
  `supplier_name` varchar(100) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`inventory_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,'OPI Red Polish','OPI','Polish','Big Apple Red',25,8.50,15.00,5,'Beauty Supply Co','2025-07-19 05:09:18'),(2,'Essie Pink Polish','Essie','Polish','Ballet Slippers',20,7.00,12.00,5,'Nail Distributors','2025-07-19 05:09:18'),(3,'Base Coat','CND','Treatment',NULL,15,6.00,10.00,3,'Professional Nails Inc','2025-07-19 05:09:18'),(4,'Top Coat','CND','Treatment',NULL,18,6.50,11.00,3,'Professional Nails Inc','2025-07-19 05:09:18'),(5,'Nail Files','Generic','Tools',NULL,50,0.75,2.00,10,'Salon Supplies LLC','2025-07-19 05:09:18'),(6,'Cuticle Oil','OPI','Treatment',NULL,12,4.00,8.00,3,'Beauty Supply Co','2025-07-19 05:09:18'),(7,'Cotton Pads','Generic','Supplies',NULL,100,0.25,1.00,20,'General Supply','2025-07-19 05:09:18'),(8,'Acetone','Zoya','Remover',NULL,8,3.00,6.00,2,'Chemical Supply Co','2025-07-19 05:09:18'),(9,'Gel Polish Blue','Gelish','Gel','Ocean Blue',22,12.00,20.00,5,'Gel Systems Ltd','2025-07-19 05:09:18'),(10,'Nail Glue','Kiss','Adhesive',NULL,30,1.50,4.00,8,'Nail Repair Co','2025-07-19 05:09:18');
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `amount` decimal(8,2) NOT NULL,
  `tip_amount` decimal(6,2) DEFAULT '0.00',
  `payment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `transaction_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `appointment_id` (`appointment_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`appointment_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,11,'Credit Card',45.00,8.00,'2024-07-22 17:15:00','TXN20240722001'),(2,12,'Cash',35.00,5.00,'2024-07-22 18:45:00','CASH20240722002'),(3,13,'Credit Card',60.00,12.00,'2024-07-23 22:15:00','TXN20240723003'),(4,14,'Debit Card',25.00,3.00,'2024-07-23 23:45:00','DBT20240723004'),(5,15,'Credit Card',55.00,10.00,'2024-07-24 19:45:00','TXN20240724005'),(7,17,'Credit Card',40.00,7.00,'2024-07-25 17:45:00','TXN20240725007'),(8,18,'Debit Card',35.00,6.00,'2024-07-25 22:45:00','DBT20240725008'),(9,19,'Cash',25.00,4.00,'2024-07-26 18:15:00','CASH20240726009'),(10,20,'Credit Card',40.00,8.00,'2024-07-27 00:15:00','TXN20240726010'),(31,1011,'card',20.00,23.00,'2025-08-21 02:25:21','dc');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `appointment_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `rating` int NOT NULL,
  `comment` text,
  `review_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,11,11,1,5,'Amazing service! Linda did a fantastic job on my nails. Very professional and friendly.','2024-07-23 01:30:00'),(2,12,12,3,4,'Good quality work. Jessica was skilled and the salon was clean. Will come back.','2024-07-23 03:15:00'),(3,13,13,2,5,'Absolutely love my spa pedicure! Emily was so gentle and the massage was relaxing.','2024-07-24 02:45:00'),(4,14,14,1,3,'Quick service but polish chipped after 2 days. Expected better quality.','2024-07-24 17:30:00'),(5,15,15,4,5,'Sophia did an incredible job on my acrylic set! Perfect length and shape.','2024-07-25 03:00:00'),(6,16,16,2,4,'Nice French manicure. Emily was professional and the result looks great.','2024-07-25 16:15:00'),(7,17,17,3,5,'Best pedicure I have ever had! Jessica was amazing and very thorough.','2024-07-26 01:30:00'),(8,18,18,1,4,'Good gel manicure. Linda was efficient and the color selection was great.','2024-07-26 15:45:00'),(9,19,19,5,2,'Service was okay but felt rushed. Manicure was basic, nothing special.','2024-07-26 22:20:00'),(10,20,20,2,5,'Emily created beautiful nail art! So creative and exactly what I wanted.','2024-07-27 19:00:00'),(12,1003,1007,5,3,'good','2025-08-20 07:16:11'),(13,1006,1012,5,5,'good','2025-08-21 02:43:05'),(14,1007,1013,5,3,'good','2025-08-21 02:57:24'),(17,11,1011,8,4,'good','2025-08-22 13:40:26');
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `service_name` varchar(100) NOT NULL,
  `description` text,
  `base_price` decimal(8,2) NOT NULL,
  `duration_minutes` int NOT NULL,
  `category` varchar(50) NOT NULL,
  `requies_appointment` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (1,'Polish Change','Simple polish removal and new color application',15.00,20,'Basic',1),(2,'Cuticle Treatment','Professional cuticle care and conditioning',20.00,25,'Treatment',1),(3,'Paraffin Treatment','Moisturizing paraffin wax treatment for hands or feet',25.00,30,'Treatment',1),(4,'Gel Removal','Safe removal of existing gel polish',12.00,20,'Removal',1),(5,'Classic Manicure','Basic nail shaping, cuticle care, and polish application',25.00,45,'Manicure',1),(6,'Gel Manicure','Long-lasting gel polish application with UV curing',35.00,60,'Manicure',1),(7,'French Manicure','Classic white tip design with clear or nude base',30.00,50,'Manicure',1),(8,'Acrylic Full Set','Complete acrylic nail extension application',55.00,90,'Extensions',1),(9,'Classic Pedicure','Foot soak, nail care, and polish with relaxing massage',40.00,60,'Pedicure',1),(10,'Spa Pedicure','Deluxe pedicure with exfoliation and extended massage',60.00,75,'Pedicure',1),(11,'Nail Art Design','Custom artistic nail designs and decorations',15.00,30,'Art',1);
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `staff_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `hire_date` date NOT NULL,
  `position` varchar(50) NOT NULL,
  `commission_rate` decimal(5,2) DEFAULT '0.15',
  `specialty` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  KEY `idx_staff_user_id` (`user_id`),
  CONSTRAINT `fk_staff_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'Linda','Miao','206-565-0200','linda.miao@beautynailnet.com','2024-06-13','Junior Nail Technician',0.12,'Basic Manicures',1,12),(2,'Emily','Rodriguez','206-555-0201','emily.rodriguez@beautynailnet.com','2023-06-15','Senior Nail Technician',0.20,'Gel Manicures',1,13),(3,'Jessica','Chen','206-555-0202','jessica.chen@beautynailnet.com','2023-08-20','Nail Technician',0.15,'Pedicures',1,14),(4,'Sophia','Kim','206-555-0203','sophia.kim@beautynailnet.com','2024-01-10','Nail Artist',0.18,'Nail Art Design',1,15),(5,'Madison','Thompson','206-555-0204','madison.thompson@beautynailnet.com','2023-09-05','Senior Technician',0.20,'Acrylic Extensions',1,16),(6,'Ashley','Garcia','206-555-0205','ashley.garcia@beautynailnet.com','2024-02-01','Nail Technician',0.15,'Classic Manicures',1,17),(7,'Taylor','White','206-555-0206','taylor.white@beautynailnet.com','2023-07-12','Spa Technician',0.17,'Spa Pedicures',1,18),(8,'Olivia','Martinez','206-555-0207','olivia.martinez@beautynailnet.com','2023-11-20','Nail Technician',0.15,'French Manicures',1,19),(9,'Hannah','Lee','206-555-0208','hannah.lee@beautynailnet.com','2024-01-25','Junior Technician',0.12,'Basic Manicures',1,20),(10,'Megan','Jackson','206-555-0209','megan.jackson@beautynailnet.com','2023-10-15','Manager',0.25,'All Services',1,21);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-22 12:36:51
