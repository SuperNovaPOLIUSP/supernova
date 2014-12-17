-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: supernova
-- ------------------------------------------------------
-- Server version	5.5.37-0ubuntu0.12.04.1

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
-- Table structure for table `academicProgram`
--

DROP TABLE IF EXISTS `academicProgram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `academicProgram` (
  `idAcademicProgram` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `vacancyNumber` int(4) DEFAULT NULL,
  `abbreviation` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  PRIMARY KEY (`idAcademicProgram`)
) ENGINE=InnoDB AUTO_INCREMENT=98002 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `aggr_offer`
--

DROP TABLE IF EXISTS `aggr_offer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aggr_offer` (
  `idOffer` int(11) NOT NULL AUTO_INCREMENT,
  `idCourse` int(11) NOT NULL,
  `idProfessor` int(11) NOT NULL,
  `idTimePeriod` int(11) NOT NULL,
  `classNumber` int(10) NOT NULL,
  `practical` tinyint(1) NOT NULL,
  `numberOfRegistrations` int(11) DEFAULT NULL,
  PRIMARY KEY (`idOffer`,`idCourse`,`idProfessor`,`idTimePeriod`,`classNumber`,`practical`),
  KEY `fk_idCourse_aggr_offer` (`idCourse`),
  KEY `fk_idProfessor_aggr_offer` (`idProfessor`),
  KEY `fk_idTimePeriod_aggr_offer` (`idTimePeriod`),
  CONSTRAINT `fk_idCourse_aggr_offer` FOREIGN KEY (`idCourse`) REFERENCES `course` (`idCourse`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idProfessor_aggr_offer` FOREIGN KEY (`idProfessor`) REFERENCES `professor` (`idProfessor`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idTimePeriod_aggr_offer` FOREIGN KEY (`idTimePeriod`) REFERENCES `timePeriod` (`idTimePeriod`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=37020 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `aggr_opticalSheetField`
--

DROP TABLE IF EXISTS `aggr_opticalSheetField`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aggr_opticalSheetField` (
  `idOpticalSheetField` int(11) NOT NULL AUTO_INCREMENT,
  `idOpticalSheet` int(11) NOT NULL,
  `idOffer` int(11) NOT NULL,
  `code` int(11) DEFAULT NULL,
  `courseIndex` int(11) DEFAULT NULL,
  PRIMARY KEY (`idOpticalSheetField`),
  KEY `fk_idOffer_aggr_opticalSheetField` (`idOffer`),
  KEY `fk_idOpticalSheet_aggr_opticalSheetField` (`idOpticalSheet`),
  CONSTRAINT `fk_idOffer_rel_offer_opticalSheet` FOREIGN KEY (`idOffer`) REFERENCES `aggr_offer` (`idOffer`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idOpticalSheet_aggr_opticalSheetField` FOREIGN KEY (`idOpticalSheet`) REFERENCES `opticalSheet` (`idOpticalSheet`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=126408 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `aggr_survey`
--

DROP TABLE IF EXISTS `aggr_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aggr_survey` (
  `idSurvey` int(11) NOT NULL AUTO_INCREMENT,
  `idOpticalSheet` int(11) NOT NULL,
  `idQuestionnaire` int(11) NOT NULL,
  `assessmentNumber` int(11) NOT NULL,
  PRIMARY KEY (`idSurvey`,`idOpticalSheet`,`idQuestionnaire`,`assessmentNumber`),
  KEY `fk_idQuestionnaire_rel_opticalSheet_questionnaire` (`idQuestionnaire`),
  KEY `fk_idOpticalSheet_rel_opticalSheet_questionnaire` (`idOpticalSheet`),
  CONSTRAINT `fk_idOpticalSheet_rel_opticalSheet_questionnaire` FOREIGN KEY (`idOpticalSheet`) REFERENCES `opticalSheet` (`idOpticalSheet`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idQuestionnaire_rel_opticalSheet_questionnaire` FOREIGN KEY (`idQuestionnaire`) REFERENCES `questionnaire` (`idQuestionnaire`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1326 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alternativeMeaning`
--

DROP TABLE IF EXISTS `alternativeMeaning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alternativeMeaning` (
  `idAlternativeMeaning` int(11) NOT NULL AUTO_INCREMENT,
  `idAnswerType` int(11) NOT NULL,
  `alternative` char(1) COLLATE utf8_unicode_ci NOT NULL,
  `meaning` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`idAlternativeMeaning`),
  KEY `fk_idAnswerType_choiceMeaning` (`idAnswerType`),
  CONSTRAINT `fk_idAnswerType_choiceMeaning` FOREIGN KEY (`idAnswerType`) REFERENCES `answerType` (`idAnswerType`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=287 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer` (
  `idAnswer` int(11) NOT NULL AUTO_INCREMENT,
  `questionIndex` int(11) NOT NULL,
  `idDatafile` int(11) NOT NULL,
  `alternative` char(1) COLLATE utf8_unicode_ci NOT NULL,
  `identifier` int(5) NOT NULL,
  PRIMARY KEY (`idAnswer`),
  KEY `fk_idDatafile_answer` (`idDatafile`),
  CONSTRAINT `fk_idDatafile_answer` FOREIGN KEY (`idDatafile`) REFERENCES `datafile` (`idDatafile`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3751364 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `answerType`
--

DROP TABLE IF EXISTS `answerType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answerType` (
  `idAnswerType` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idAnswerType`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `classRepresentative`
--

DROP TABLE IF EXISTS `classRepresentative`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classRepresentative` (
  `idClassRepresentative` int(11) NOT NULL AUTO_INCREMENT COMMENT '		',
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `memberId` int(11) NOT NULL COMMENT '	',
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `cellphoneNumber` int(10) DEFAULT NULL,
  PRIMARY KEY (`idClassRepresentative`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `idCourse` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `abbreviation` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `syllabus` text COLLATE utf8_unicode_ci,
  `courseCode` char(7) COLLATE utf8_unicode_ci NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  PRIMARY KEY (`idCourse`),
  KEY `courseCode` (`courseCode`)
) ENGINE=InnoDB AUTO_INCREMENT=14296 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `courseCoordination`
--

DROP TABLE IF EXISTS `courseCoordination`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseCoordination` (
  `idCourseCoordination` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `abbreviation` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`idCourseCoordination`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Comissão de Curso. Tabela que guarda cada uma das comissões ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cycle`
--

DROP TABLE IF EXISTS `cycle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cycle` (
  `idCycle` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `abbreviation` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `idCycleType` int(11) NOT NULL,
  `vacancyNumber` int(4) DEFAULT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `cycleCode` int(10) NOT NULL,
  `dayPeriod` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `termLength` int(11) NOT NULL,
  PRIMARY KEY (`idCycle`),
  KEY `fk_idCycleType` (`idCycleType`),
  KEY `fk_termLength` (`termLength`),
  CONSTRAINT `fk_idCycleType` FOREIGN KEY (`idCycleType`) REFERENCES `minitableCycleType` (`idCycleType`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_termLength` FOREIGN KEY (`termLength`) REFERENCES `minitableLength` (`idLength`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=441 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dataAnalysisReport`
--

DROP TABLE IF EXISTS `dataAnalysisReport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dataAnalysisReport` (
  `idDataAnalysisReport` int(11) NOT NULL AUTO_INCREMENT,
  `idOffer` int(11) NOT NULL,
  `idClassRepresentative` int(11) NOT NULL,
  `dataAnalysisReport` text COLLATE utf8_unicode_ci NOT NULL,
  `submissionTime` datetime DEFAULT NULL,
  PRIMARY KEY (`idDataAnalysisReport`,`idOffer`,`idClassRepresentative`),
  KEY `fk_idOffer_dataAnalysisReport` (`idOffer`),
  KEY `fk_idClassRepresentative_dataAnalysisReport` (`idClassRepresentative`),
  CONSTRAINT `fk_idClassRepresentative_dataAnalysisReport` FOREIGN KEY (`idClassRepresentative`) REFERENCES `classRepresentative` (`idClassRepresentative`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idOffer_dataAnalysisReport` FOREIGN KEY (`idOffer`) REFERENCES `aggr_offer` (`idOffer`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `datafile`
--

DROP TABLE IF EXISTS `datafile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datafile` (
  `idDatafile` int(11) NOT NULL AUTO_INCREMENT,
  `fileName` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idDatafile`)
) ENGINE=InnoDB AUTO_INCREMENT=1580 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `department` (
  `idDepartment` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `departmentCode` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idDepartment`),
  KEY `departmentCode` (`departmentCode`)
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `encoding`
--

DROP TABLE IF EXISTS `encoding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encoding` (
  `idOpticalSheet` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idOpticalSheet`),
  CONSTRAINT `fk_idOpticalSheet_encoding` FOREIGN KEY (`idOpticalSheet`) REFERENCES `opticalSheet` (`idOpticalSheet`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faculty` (
  `idFaculty` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `abbreviation` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `campus` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`idFaculty`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `minitableCycleType`
--

DROP TABLE IF EXISTS `minitableCycleType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `minitableCycleType` (
  `idCycleType` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idCycleType`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `minitableDayOfTheWeek`
--

DROP TABLE IF EXISTS `minitableDayOfTheWeek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `minitableDayOfTheWeek` (
  `idDayOfTheWeek` int(11) NOT NULL AUTO_INCREMENT,
  `dayOfTheWeek` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idDayOfTheWeek`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `minitableLength`
--

DROP TABLE IF EXISTS `minitableLength`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `minitableLength` (
  `idLength` int(11) NOT NULL AUTO_INCREMENT,
  `length` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idLength`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `minitableRequirementType`
--

DROP TABLE IF EXISTS `minitableRequirementType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `minitableRequirementType` (
  `idRequirementType` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idRequirementType`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `minitableRequisitionType`
--

DROP TABLE IF EXISTS `minitableRequisitionType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `minitableRequisitionType` (
  `idRequisitionType` int(11) NOT NULL AUTO_INCREMENT,
  `requisitionType` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idRequisitionType`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `minitableSurveyType`
--

DROP TABLE IF EXISTS `minitableSurveyType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `minitableSurveyType` (
  `idSurveyType` int(11) NOT NULL AUTO_INCREMENT,
  `typeName` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idSurveyType`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `opticalSheet`
--

DROP TABLE IF EXISTS `opticalSheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opticalSheet` (
  `idOpticalSheet` int(11) NOT NULL AUTO_INCREMENT,
  `idSurveyType` int(11) NOT NULL,
  PRIMARY KEY (`idOpticalSheet`),
  KEY `fk_idSurveyType_opticalSheet` (`idSurveyType`),
  CONSTRAINT `fk_idSurveyType_opticalSheet` FOREIGN KEY (`idSurveyType`) REFERENCES `minitableSurveyType` (`idSurveyType`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1516 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `professor`
--

DROP TABLE IF EXISTS `professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `professor` (
  `idProfessor` int(11) NOT NULL AUTO_INCREMENT,
  `memberId` int(10) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `office` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(65) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phoneNumber` int(10) DEFAULT NULL,
  `cellphoneNumber` int(10) DEFAULT NULL,
  PRIMARY KEY (`idProfessor`),
  KEY `memberId` (`memberId`)
) ENGINE=InnoDB AUTO_INCREMENT=7571 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question` (
  `idQuestion` int(11) NOT NULL AUTO_INCREMENT,
  `idAnswerType` int(11) NOT NULL,
  `questionWording` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idQuestion`,`idAnswerType`),
  KEY `fk_idAnswerType_question` (`idAnswerType`),
  CONSTRAINT `fk_idAnswerType_question` FOREIGN KEY (`idAnswerType`) REFERENCES `answerType` (`idAnswerType`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=786 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `questionnaire`
--

DROP TABLE IF EXISTS `questionnaire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questionnaire` (
  `idQuestionnaire` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `creationDate` date NOT NULL,
  PRIMARY KEY (`idQuestionnaire`)
) ENGINE=InnoDB AUTO_INCREMENT=1148 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_academicProgram_cycle`
--

DROP TABLE IF EXISTS `rel_academicProgram_cycle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_academicProgram_cycle` (
  `idAcademicProgram` int(11) NOT NULL,
  `idCycle` int(11) NOT NULL,
  PRIMARY KEY (`idAcademicProgram`,`idCycle`),
  KEY `fk_idCycle_rel_academicProgram_cycle` (`idCycle`),
  KEY `fk_idAcademicProgram_rel_academicProgram_cycle` (`idAcademicProgram`),
  CONSTRAINT `fk_idAcademicProgram` FOREIGN KEY (`idAcademicProgram`) REFERENCES `academicProgram` (`idAcademicProgram`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idCycle_rel_academicProgram_cycle` FOREIGN KEY (`idCycle`) REFERENCES `cycle` (`idCycle`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_answer_opticalSheetField_survey`
--

DROP TABLE IF EXISTS `rel_answer_opticalSheetField_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_answer_opticalSheetField_survey` (
  `idAnswer` int(11) NOT NULL,
  `idOpticalSheetField` int(11) NOT NULL,
  `idSurvey` int(11) NOT NULL,
  PRIMARY KEY (`idAnswer`,`idOpticalSheetField`,`idSurvey`),
  KEY `fk_idOpticalSheetField_aggr_opticalSheetField` (`idOpticalSheetField`),
  KEY `fk_idSurvey_survey` (`idSurvey`),
  CONSTRAINT `fk_idAnswer_answer` FOREIGN KEY (`idAnswer`) REFERENCES `answer` (`idAnswer`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idOpticalSheetField_aggr_opticalSheetField` FOREIGN KEY (`idOpticalSheetField`) REFERENCES `aggr_opticalSheetField` (`idOpticalSheetField`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idSurvey_survey` FOREIGN KEY (`idSurvey`) REFERENCES `aggr_survey` (`idSurvey`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_classRepresentative_opticalSheet`
--

DROP TABLE IF EXISTS `rel_classRepresentative_opticalSheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_classRepresentative_opticalSheet` (
  `idClassRepresentative` int(11) NOT NULL,
  `idOpticalSheet` int(11) NOT NULL,
  PRIMARY KEY (`idClassRepresentative`,`idOpticalSheet`),
  KEY `fk_idClassRepresentative_rel_classRepresentative_opticalSheet` (`idClassRepresentative`),
  KEY `fk_idOpticalSheet_rel_classRepresentative_opticalSheet` (`idOpticalSheet`),
  CONSTRAINT `fk_idClassRepresentative_rel_classRepresentative_opticalSheet` FOREIGN KEY (`idClassRepresentative`) REFERENCES `classRepresentative` (`idClassRepresentative`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idOpticalSheet_rel_classRepresentative_opticalSheet` FOREIGN KEY (`idOpticalSheet`) REFERENCES `opticalSheet` (`idOpticalSheet`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_courseCoordination_cycle`
--

DROP TABLE IF EXISTS `rel_courseCoordination_cycle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_courseCoordination_cycle` (
  `idCourseCoordination` int(11) NOT NULL,
  `idCycle` int(11) NOT NULL,
  PRIMARY KEY (`idCourseCoordination`,`idCycle`),
  KEY `fk_idCycle_rel_courseCoordination_cycle` (`idCycle`),
  KEY `fk_idCourseCoordination` (`idCourseCoordination`),
  CONSTRAINT `fk_idCourseCoordination_rel_courseCoordination_cycle` FOREIGN KEY (`idCourseCoordination`) REFERENCES `courseCoordination` (`idCourseCoordination`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idCycle_rel_courseCoordination_cycle` FOREIGN KEY (`idCycle`) REFERENCES `cycle` (`idCycle`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_courseCoordination_faculty`
--

DROP TABLE IF EXISTS `rel_courseCoordination_faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_courseCoordination_faculty` (
  `idCourseCoordination` int(11) NOT NULL,
  `idFaculty` int(11) NOT NULL,
  PRIMARY KEY (`idCourseCoordination`,`idFaculty`),
  KEY `fk_idFaculty_rel_courseCoordination_faculty` (`idFaculty`),
  CONSTRAINT `fk_idCourseCoordination_rel_courseCoordination_faculty` FOREIGN KEY (`idCourseCoordination`) REFERENCES `courseCoordination` (`idCourseCoordination`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idFaculty_rel_courseCoordination_faculty` FOREIGN KEY (`idFaculty`) REFERENCES `faculty` (`idFaculty`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_course_cycle`
--

DROP TABLE IF EXISTS `rel_course_cycle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_course_cycle` (
  `idCourse` int(11) NOT NULL,
  `idCycle` int(11) NOT NULL,
  `term` tinyint(4) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `requisitionType` int(11) DEFAULT NULL,
  PRIMARY KEY (`idCourse`,`idCycle`,`term`,`endDate`),
  KEY `fk_idCycle_rel_course_cycle` (`idCycle`),
  KEY `fk_idCourse` (`idCourse`),
  KEY `fk_idRequisitionType` (`requisitionType`),
  CONSTRAINT `fk_idCourse_rel_course_cycle` FOREIGN KEY (`idCourse`) REFERENCES `course` (`idCourse`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idCycle_rel_course_cycle` FOREIGN KEY (`idCycle`) REFERENCES `cycle` (`idCycle`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idRequisitionType` FOREIGN KEY (`requisitionType`) REFERENCES `minitableRequisitionType` (`idRequisitionType`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_course_cycle_course`
--

DROP TABLE IF EXISTS `rel_course_cycle_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_course_cycle_course` (
  `idCycle` int(11) NOT NULL COMMENT '		',
  `idCourse` int(11) NOT NULL,
  `idRequirement` int(11) NOT NULL,
  `idRequirementType` int(11) NOT NULL,
  PRIMARY KEY (`idCycle`,`idCourse`,`idRequirement`),
  KEY `fk_idCourse` (`idCourse`),
  KEY `fk_idRequirement` (`idRequirement`),
  KEY `fk_idRequirementType` (`idRequirementType`),
  CONSTRAINT `fk_idCourse` FOREIGN KEY (`idCourse`) REFERENCES `course` (`idCourse`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idCycle` FOREIGN KEY (`idCycle`) REFERENCES `cycle` (`idCycle`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idRequirement` FOREIGN KEY (`idRequirement`) REFERENCES `course` (`idCourse`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idRequirementType` FOREIGN KEY (`idRequirementType`) REFERENCES `minitableRequirementType` (`idRequirementType`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_cycle_opticalSheet`
--

DROP TABLE IF EXISTS `rel_cycle_opticalSheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_cycle_opticalSheet` (
  `idOpticalSheet` int(11) NOT NULL,
  `idCycle` int(10) NOT NULL,
  `term` int(11) NOT NULL,
  PRIMARY KEY (`idOpticalSheet`,`idCycle`,`term`),
  KEY `fk_idCycle_rel_cycle_opticalSheet` (`idCycle`),
  CONSTRAINT `fk_idCycle_rel_cycle_opticalSheet` FOREIGN KEY (`idCycle`) REFERENCES `cycle` (`idCycle`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idOpticalSheet_rel_cycle_opticalSheet` FOREIGN KEY (`idOpticalSheet`) REFERENCES `opticalSheet` (`idOpticalSheet`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_department_professor`
--

DROP TABLE IF EXISTS `rel_department_professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_department_professor` (
  `idProfessor` int(11) NOT NULL,
  `idDepartment` int(11) NOT NULL,
  PRIMARY KEY (`idProfessor`,`idDepartment`),
  KEY `fk_idDepartment_rel_department_professor` (`idDepartment`),
  KEY `fk_idProfessor_rel_department_professor` (`idProfessor`),
  CONSTRAINT `fk_idDepartment_rel_department_professor` FOREIGN KEY (`idDepartment`) REFERENCES `department` (`idDepartment`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idProfessor_rel_department_professor` FOREIGN KEY (`idProfessor`) REFERENCES `professor` (`idProfessor`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_offer_schedule`
--

DROP TABLE IF EXISTS `rel_offer_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_offer_schedule` (
  `idSchedule` int(11) NOT NULL,
  `idOffer` int(11) NOT NULL,
  PRIMARY KEY (`idSchedule`,`idOffer`),
  KEY `fk_idSchedule` (`idSchedule`),
  KEY `fk_idOffer_rel_aggr_offer_schedule` (`idOffer`),
  CONSTRAINT `fk_idOffer_rel_aggr_offer_schedule` FOREIGN KEY (`idOffer`) REFERENCES `aggr_offer` (`idOffer`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idSchedule` FOREIGN KEY (`idSchedule`) REFERENCES `schedule` (`idSchedule`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rel_question_questionnaire`
--

DROP TABLE IF EXISTS `rel_question_questionnaire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rel_question_questionnaire` (
  `idQuestionnaire` int(11) NOT NULL,
  `idQuestion` int(11) NOT NULL,
  `questionIndex` int(11) NOT NULL,
  PRIMARY KEY (`idQuestionnaire`,`idQuestion`),
  KEY `fk_idQuestionnaire_rel_question_questionnaire` (`idQuestionnaire`),
  KEY `fk_idQuestion_rel_question_questionnaire` (`idQuestion`),
  CONSTRAINT `fk_idQuestionnaire_rel_question_questionnaire` FOREIGN KEY (`idQuestionnaire`) REFERENCES `questionnaire` (`idQuestionnaire`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_idQuestion_rel_question_questionnaire` FOREIGN KEY (`idQuestion`) REFERENCES `question` (`idQuestion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `respostascalc1`
--

DROP TABLE IF EXISTS `respostascalc1`;
/*!50001 DROP VIEW IF EXISTS `respostascalc1`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `respostascalc1` (
  `idAnswer` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule` (
  `idSchedule` int(11) NOT NULL AUTO_INCREMENT,
  `idDayOfTheWeek` int(11) NOT NULL,
  `start` time NOT NULL,
  `end` time NOT NULL,
  `frequency` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idSchedule`),
  KEY `fk_idDayOfTheWeek_schedule` (`idDayOfTheWeek`),
  CONSTRAINT `fk_idDayOfTheWeek_schedule` FOREIGN KEY (`idDayOfTheWeek`) REFERENCES `minitableDayOfTheWeek` (`idDayOfTheWeek`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1441 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `timePeriod`
--

DROP TABLE IF EXISTS `timePeriod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timePeriod` (
  `idTimePeriod` int(11) NOT NULL AUTO_INCREMENT,
  `length` int(1) NOT NULL,
  `year` int(4) NOT NULL,
  `session` int(1) NOT NULL,
  PRIMARY KEY (`idTimePeriod`),
  KEY `idLenght_timePeriod` (`length`),
  CONSTRAINT `idLenght_timePeriod` FOREIGN KEY (`length`) REFERENCES `minitableLength` (`idLength`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `respostascalc1`
--

/*!50001 DROP TABLE IF EXISTS `respostascalc1`*/;
/*!50001 DROP VIEW IF EXISTS `respostascalc1`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`ae`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `respostascalc1` AS select `rel_answer_opticalSheetField_survey`.`idAnswer` AS `idAnswer` from `rel_answer_opticalSheetField_survey` where (`rel_answer_opticalSheetField_survey`.`idOpticalSheetField` = 113308) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-12-09 11:50:24
