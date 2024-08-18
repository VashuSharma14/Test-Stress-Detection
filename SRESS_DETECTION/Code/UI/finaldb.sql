userdetailes/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - crudeoil
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`Stressdection` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `Stressdection`;

/*Table structure for table `userdetailes` */

DROP TABLE IF EXISTS `userdetailes`;

CREATE TABLE `userdetailes` (
  `Id` int(255) NOT NULL auto_increment,
  `name` varchar(255) default NULL,
  `address` varchar(255) default NULL,
  `phone` varchar(255) default NULL,
  `email` varchar(255) default NULL,
  `password` varchar(255) default NULL,
  `filenamepath` varchar(255) default NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `userdetailes` */

insert  into `userdetailes`(`Id`,`name`,`address`,`phone`,`email`,`password`,`filenamepath`) values (1,'yash','mumbai','9632587414','a@gmail.com','a','static/Profile/person_2-min.jpg'),(2,'amey','mumbai','7894561232','jackspaarow51@gmail.com','a','static/Profile/2.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
