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
  `optimalClusters` int(2) DEFAULT NULL,
  `clustersDetail` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`clustersDetail`)),
  UNIQUE KEY `id_sample` (`id`),
  KEY `fk_users` (`idUser`),
  CONSTRAINT `fk_users` FOREIGN KEY (`idUser`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

DROP TABLE IF EXISTS `records`;
CREATE TABLE `records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `followID` int(11) NOT NULL,
  `sampleRoute` varchar(255) NOT NULL,
  `countCol` int(11) NOT NULL,
  `dayNumber` int(11) DEFAULT NULL,
  `creationTime` time DEFAULT current_timestamp(),
  `creationDate` date DEFAULT NULL,
  `state` int(1) DEFAULT NULL,
  `processingTime` float DEFAULT NULL,
  `clustersDetail` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`clustersDetail`)),
  `optimalClusters` int(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_follow` (`followID`),
  CONSTRAINT `fk_follow` FOREIGN KEY (`followID`) REFERENCES `follows` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;



INSERT INTO `follows` (`id`, `name`, `idUser`, `description`, `creationDate`, `state`, `creationTime`) VALUES
(13, 'Bacteria X', 19, 'Poliferacion de una colonia', '2026-04-27', 1, '14:07:18'),
(14, 'Bacteria A', 19, 'aaa', '2026-04-27', 1, '16:43:38');
INSERT INTO `records` (`id`, `followID`, `sampleRoute`, `countCol`, `dayNumber`, `creationTime`, `creationDate`, `state`, `processingTime`, `clustersDetail`, `optimalClusters`) VALUES
(26, 13, 'd71d7d154d2e4de9bca034796f9073b4_34.png', 15, 1, '14:14:06', '2026-04-27', 1, 0.71969, '{\"1\": {\"count\": 56, \"percentage\": 42.11}, \"0\": {\"count\": 77, \"percentage\": 57.89}}', 0),
(27, 13, '77ee07d7ad834c7e822829d9cb9ee1a9_35.jpg', 20, 2, '14:16:30', '2026-04-27', 1, 0.978223, '{\"1\": {\"count\": 56, \"percentage\": 42.11}, \"0\": {\"count\": 77, \"percentage\": 57.89}}', 2),
(28, 13, 'd63c9ea935b3469db868b73cf8a2c23f_34.png', 35, 3, '14:19:21', '2026-04-27', 1, 1.81469, '{\"1\": {\"count\": 56, \"percentage\": 42.11}, \"0\": {\"count\": 77, \"percentage\": 57.89}}', 0),
(29, 13, 'dd6660c5c639443bb001cb3e6a667fbb_33.jpg', 50, 4, '14:27:55', '2026-04-27', 1, 0.491845, '{\"0\": {\"count\": 2, \"percentage\": 100.0}}', 1),
(30, 13, '1cb27f6da1e54ecf8d5f69bf21e4ee52_35.jpg', 90, 5, '14:42:15', '2026-04-27', 1, 0.82318, '{\"1\": {\"count\": 56, \"percentage\": 42.11}, \"0\": {\"count\": 77, \"percentage\": 57.89}}', 2),
(31, 13, 'feb1a4c52af5497e9064820dd470b9d1_35.jpg', 133, 8, '16:37:34', '2026-04-27', 1, 1.10309, '{\"1\": {\"count\": 56, \"percentage\": 42.11}, \"0\": {\"count\": 77, \"percentage\": 57.89}}', 2),
(32, 13, '6cb2cb0dd84f44dda61ae9dd469e245d_33.jpg', 2, 9, '16:39:33', '2026-04-27', 1, 0.573732, '{\"0\": {\"count\": 2, \"percentage\": 100.0}}', 1),
(33, 14, '53f5a098b0214a7f884b95ee95eb2d8c_33.jpg', 2, 1, '16:43:56', '2026-04-27', 1, 0.562251, '{\"0\": {\"count\": 2, \"percentage\": 100.0}}', 1),
(34, 14, '197b65ee411145fda6cba1fbd5b4b437_35.jpg', 133, 100, '16:44:12', '2026-04-27', 0, 1.11683, '{\"1\": {\"count\": 56, \"percentage\": 42.11}, \"0\": {\"count\": 77, \"percentage\": 57.89}}', 2),
(35, 14, '625312320f4245cb8abba97c740f3f4e_33.jpg', 2, 11, '17:35:11', '2026-04-27', 1, 1.35845, '{\"0\": {\"count\": 2, \"percentage\": 100.0}}', 1);
INSERT INTO `samples` (`id`, `sampleName`, `idUser`, `typeSample`, `volumenSample`, `factorSample`, `sampleRoute`, `creationDate`, `processingTime`, `count`, `creationTime`, `medioSample`, `state`, `optimalClusters`, `clustersDetail`) VALUES
(108, 'Muestra 10', 19, 'Alimentos', '1', '1', '2c29f52cd0044e41926a271f81cec06e_35.jpg', '2026-04-27', 0.816931, 133, '13:59:41', 'Agar MacConkey', 1, 2, '{\"1\": {\"count\": 56, \"percentage\": 42.11}, \"0\": {\"count\": 77, \"percentage\": 57.89}}');
INSERT INTO `users` (`id`, `name`, `lastname`, `email`, `password`, `username`, `type`) VALUES
(19, 'Luis Alberto', 'Jimenez Villa', 'luisjivl@gmail.com', '$2b$12$rE7PF4JHJVBBFN86FZiQeONQbT9AIYUfaui/4KIn3l54wAc/sWLc6', 'LuisVilla', 1);

