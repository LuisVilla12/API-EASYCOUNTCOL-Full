/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

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


INSERT INTO `follows` (`id`, `name`, `idUser`, `description`, `creationDate`, `state`, `creationTime`) VALUES
(1, 'Seguimiento 1', 19, 'Prueba', '2026-04-23', 0, '17:42:25'),
(2, 'Bacteria D', 19, 'Prueba 7', '2026-04-25', 1, '17:42:25'),
(3, 'Bacteria B', 19, 'Pruebas de bacterias B', '2026-04-24', 1, '17:58:58'),
(4, 'Bacteria C', 19, 'CCCCCCCCC', '2026-04-24', 1, '17:59:02'),
(5, 'Bacteria A', 19, 'Placa de  Agarr', '2026-04-24', 1, '17:59:17'),
(6, 'Bacteria Z', 19, '1asdfasdf', '2026-04-24', 1, '18:04:23'),
(7, 'Bacteria Y', 19, 'PRUEBA', '2026-04-24', 1, '18:11:52');
INSERT INTO `samples` (`id`, `sampleName`, `idUser`, `typeSample`, `volumenSample`, `factorSample`, `sampleRoute`, `creationDate`, `processingTime`, `count`, `creationTime`, `medioSample`, `state`) VALUES
(72, 'Muestra 1', 19, 'Ambiental', '1', '1', 'c9ba7af4e1da41edade9fe4294ec8c9f_CAP9075502000971033217.jpg', '2026-04-22', 0.460042, 1, '17:42:25', 'Agar MacConkey', 0),
(73, 'Muestra 11', 19, 'Ambiental', '11', '11', 'b5ba90fe57d24e53b5db142a561288ed_33.jpg', '2026-04-22', 0.453687, 2, '17:45:44', 'Otro medio de cultivo', 0),
(74, 'Muestra 11', 19, '', '1', '1', '046f375809124f47b7d10c5ce12bb20c_CAP2446236157127779261.jpg', '2026-04-22', 0.336956, 1, '17:47:36', 'Agar sangre', 0),
(75, 'Muestra AA', 19, 'Otras', '1', '1', '2dfd3cf866964d28a3b57fc469be59c6_CAP6082908378507350592.jpg', '2026-04-22', 0.444636, 1, '17:49:34', 'Agar MacConkey', 0),
(76, 'Muestra 1', 19, 'Material', '1', '1', 'dc7d92ded9cc4fa69c5e5e39ebb5a17d_CAP734140449722890027.jpg', '2026-04-22', 0.487862, 1, '18:03:56', 'Otro', 0),
(77, 'aaa', 19, 'Ambiental', '11', '11', 'ed268e8147c4497b85a134a6ea0ec8ac_33.jpg', '2026-04-22', 0.374803, 2, '18:18:51', 'Agar MacConkey', 0),
(78, 'Muestra 2', 19, 'Clinica - Biológica', '2', '3', 'd29195d013a645e397ee30a0ec4924a1_33.jpg', '2026-04-22', 0.478673, 2, '18:28:07', 'Agar Nutritivo', 0),
(79, 'aaaaaaa', 19, 'Ambiental', '1', '1', '856222a9d54043c5bde633b1f5bebfdf_33.jpg', '2026-04-22', 0.447711, 2, '18:45:20', 'Agar MacConkey', 0),
(80, 'Muestra 4', 19, 'Ambiental', '1', '1', 'c126eb87f0a54cf0b6a6285d5743025e_33.jpg', '2026-04-23', 0.877224, 2, '16:54:35', 'Agar MacConkey', 0),
(81, 'Muestra 19', 19, 'Otro', '1', '1', '148ffdd26a034f1894934fd42bfe9cc5_35.jpg', '2026-04-24', 1.14882, 133, '14:18:01', 'Otro', 1);
INSERT INTO `users` (`id`, `name`, `lastname`, `email`, `password`, `username`, `type`) VALUES
(19, 'Luis Alberto', 'Jimenez Villa', 'luisjivl@gmail.com', '$2b$12$rE7PF4JHJVBBFN86FZiQeONQbT9AIYUfaui/4KIn3l54wAc/sWLc6', 'LuisVilla', 1);


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;