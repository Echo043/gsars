-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: gsars
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `SID` int NOT NULL,
  `F_name` varchar(255) DEFAULT NULL,
  `M_name` varchar(255) DEFAULT NULL,
  `L_name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Programme` varchar(255) DEFAULT NULL,
  `Year` int DEFAULT NULL,
  `Semester` varchar(255) DEFAULT NULL,
  `Sl_no` int DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`SID`),
  KEY `Sl_no` (`Sl_no`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`Sl_no`) REFERENCES `admin` (`Sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (12190001,'hello','chaodr','tenz','12190001.gcit@rub.edu.bt','before','yo',2222,'srping',NULL,'student'),(12190002,'chador','tenzin','tenzin','12190001.gcit@rub.edu.bt','hello','yo',2222,'',NULL,'student'),(12190004,'chador','-','tenzin','howiam4u@gmail.com','hello','yo',2222,'',NULL,'Student'),(12190018,'Rinchen ','-','Thinley','12190018.gcit@rub.edu.bt','rannas','Bsc. Computer Science',2022,'',NULL,'Student'),(12190019,'Samten ','','Gyeltshen','12190001.gcit@rub.edu.bt','rannas','yo',2222,'',NULL,'Student'),(12190020,'chador','chaodr','Gyeltshen','121900.gcit@rub.edu.bt','rinchen','Bsc. Computer Science',2222,'',NULL,'Student');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-04 16:05:27
