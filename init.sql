/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

use easycountcol;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(155) NOT NULL,
  `lastname` varchar(155) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `type` int(11) DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `samples`;
CREATE TABLE `samples` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sampleName` varchar(150) NOT NULL,
  `idUser` int(11) NOT NULL,
  `typeSample` varchar(255) NOT NULL,
  `volumenSample` varchar(255) NOT NULL,
  `factorSample` varchar(255) NOT NULL,
  `sampleRoute` varchar(255) NOT NULL,
  `creationDate` date NOT NULL,
  `processingTime` float NOT NULL,
  `count` int(4) NOT NULL,
  `creationTime` time DEFAULT NULL,
  `medioSample` varchar(255) NOT NULL,
  `state` int(1) DEFAULT NULL,
  UNIQUE KEY `id_sample` (`id`),
  KEY `fk_users` (`idUser`),
  CONSTRAINT `fk_users` FOREIGN KEY (`idUser`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `follows`;
CREATE TABLE `follows` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `idUser` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `creationDate` date DEFAULT current_timestamp(),
  `state` int(1) DEFAULT 1,
  `creationTime` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_follows_users` (`idUser`),
  CONSTRAINT `fk_follows_users` FOREIGN KEY (`idUser`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

DROP TABLE IF EXISTS `follow_records`;
CREATE TABLE `follow_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `followID` int(11) NOT NULL,
  `imagePath` varchar(255) NOT NULL,
  `colonyCount` int(11) NOT NULL,
  `dayNumber` int(11) DEFAULT NULL,
  `creationTime` time DEFAULT current_timestamp(),
  `creationDate` date DEFAULT NULL,
  `state` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_follow` (`followID`),
  CONSTRAINT `fk_follow` FOREIGN KEY (`followID`) REFERENCES `follows` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


INSERT INTO `users` (`id`, `name`, `lastname`, `email`, `password`, `username`, `type`) VALUES
(19, 'Luis Alberto', 'Jimenez Villa', 'luisjivl@gmail.com', '$2b$12$rE7PF4JHJVBBFN86FZiQeONQbT9AIYUfaui/4KIn3l54wAc/sWLc6', 'LuisVilla', 1);


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;