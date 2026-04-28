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

INSERT INTO `users` (`id`, `name`, `lastname`, `email`, `password`, `username`, `type`) VALUES
(19, 'Luis Alberto', 'Jimenez Villa', 'luisjivl@gmail.com', '$2b$12$rE7PF4JHJVBBFN86FZiQeONQbT9AIYUfaui/4KIn3l54wAc/sWLc6', 'LuisVilla', 1);

