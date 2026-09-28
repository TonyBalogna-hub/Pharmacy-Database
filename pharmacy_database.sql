-- MySQL dump 10.13  Distrib 8.4.10, for Linux (x86_64)
--
-- Host: localhost    Database: pharmacy_database
-- ------------------------------------------------------
-- Server version	8.4.10-0ubuntu0.26.04.1

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
-- Table structure for table `Medication`
--

DROP TABLE IF EXISTS `Medication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Medication` (
  `MedicationID` int unsigned NOT NULL,
  `MedicationName` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Dosage` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `QuantityInStock` int unsigned NOT NULL,
  PRIMARY KEY (`MedicationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Medication`
--

LOCK TABLES `Medication` WRITE;
/*!40000 ALTER TABLE `Medication` DISABLE KEYS */;
INSERT INTO `Medication` VALUES (1,'Amoxicillin','500 mg',90),(2,'Ibuprofen','600 mg',60),(3,'Acetaminophen','325 mg',120);
/*!40000 ALTER TABLE `Medication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MedicationForm`
--

DROP TABLE IF EXISTS `MedicationForm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MedicationForm` (
  `MedicationID` int unsigned NOT NULL,
  `FormID` int unsigned NOT NULL,
  `FormType` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Strength` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`MedicationID`,`FormID`),
  CONSTRAINT `fk_form_medication` FOREIGN KEY (`MedicationID`) REFERENCES `Medication` (`MedicationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MedicationForm`
--

LOCK TABLES `MedicationForm` WRITE;
/*!40000 ALTER TABLE `MedicationForm` DISABLE KEYS */;
INSERT INTO `MedicationForm` VALUES (1,1,'Capsule','500 mg'),(1,2,'Liquid','250 mg per 5 mL'),(2,1,'Tablet','600 mg'),(3,1,'Tablet','325 mg'),(3,2,'Liquid','160 mg per 5 mL');
/*!40000 ALTER TABLE `MedicationForm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patient`
--

DROP TABLE IF EXISTS `Patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patient` (
  `PatientID` int unsigned NOT NULL,
  `FirstName` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `LastName` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DateOfBirth` date NOT NULL,
  PRIMARY KEY (`PatientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patient`
--

LOCK TABLES `Patient` WRITE;
/*!40000 ALTER TABLE `Patient` DISABLE KEYS */;
INSERT INTO `Patient` VALUES (1,'John','Smith','1991-01-01'),(2,'Jane','Doe','1991-01-01'),(3,'Alex','Rivera','1985-06-12');
/*!40000 ALTER TABLE `Patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Prescription`
--

DROP TABLE IF EXISTS `Prescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prescription` (
  `RXNumber` int unsigned NOT NULL,
  `DrugName` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `WrittenDate` date NOT NULL,
  `QuantityPrescribed` int unsigned NOT NULL,
  `PatientID` int unsigned NOT NULL,
  `MedicationID` int unsigned NOT NULL,
  PRIMARY KEY (`RXNumber`),
  KEY `fk_prescription_patient` (`PatientID`),
  KEY `fk_prescription_medication` (`MedicationID`),
  CONSTRAINT `fk_prescription_medication` FOREIGN KEY (`MedicationID`) REFERENCES `Medication` (`MedicationID`),
  CONSTRAINT `fk_prescription_patient` FOREIGN KEY (`PatientID`) REFERENCES `Patient` (`PatientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Prescription`
--

LOCK TABLES `Prescription` WRITE;
/*!40000 ALTER TABLE `Prescription` DISABLE KEYS */;
INSERT INTO `Prescription` VALUES (1001,'Amoxicillin','2026-09-01',30,1,1),(1002,'Ibuprofen','2026-09-02',60,2,2),(1003,'Amoxicillin','2026-09-15',20,2,1),(1004,'Acetaminophen','2026-09-18',24,3,3);
/*!40000 ALTER TABLE `Prescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Supplier`
--

DROP TABLE IF EXISTS `Supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Supplier` (
  `SupplierID` int unsigned NOT NULL,
  `CompanyName` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `PhoneNumber` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Address` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`SupplierID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Supplier`
--

LOCK TABLES `Supplier` WRITE;
/*!40000 ALTER TABLE `Supplier` DISABLE KEYS */;
INSERT INTO `Supplier` VALUES (1,'ABC Pharmaceuticals','555-123-4567','123 Main Street'),(2,'Mountain Medical Supply','555-555-0128','42 Pine Avenue');
/*!40000 ALTER TABLE `Supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SupplierMedication`
--

DROP TABLE IF EXISTS `SupplierMedication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SupplierMedication` (
  `SupplierID` int unsigned NOT NULL,
  `MedicationID` int unsigned NOT NULL,
  PRIMARY KEY (`SupplierID`,`MedicationID`),
  KEY `fk_suppliermed_medication` (`MedicationID`),
  CONSTRAINT `fk_suppliermed_medication` FOREIGN KEY (`MedicationID`) REFERENCES `Medication` (`MedicationID`),
  CONSTRAINT `fk_suppliermed_supplier` FOREIGN KEY (`SupplierID`) REFERENCES `Supplier` (`SupplierID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SupplierMedication`
--

LOCK TABLES `SupplierMedication` WRITE;
/*!40000 ALTER TABLE `SupplierMedication` DISABLE KEYS */;
INSERT INTO `SupplierMedication` VALUES (1,1),(2,1),(1,2),(1,3),(2,3);
/*!40000 ALTER TABLE `SupplierMedication` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-31  4:35:22
