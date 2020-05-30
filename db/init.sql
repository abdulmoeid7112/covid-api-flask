CREATE DATABASE if not exists covid19;

use covid19;

CREATE TABLE `covid_stats_country` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `country` varchar(50) DEFAULT NULL,
  `tests` varchar(50) DEFAULT NULL,
  `cases` varchar(50) DEFAULT NULL,
  `deaths` varchar(50) DEFAULT NULL,
  `recovered` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `covid_stats_country_region` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `country_region` varchar(50) DEFAULT NULL,
  `confirmed` varchar(50) DEFAULT NULL,
  `deaths` varchar(50) DEFAULT NULL,
  `recovered` varchar(50) DEFAULT NULL,
  `last_updated` varchar(50) DEFAULT NULL,
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `covid_stats_us` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `state` varchar(50) DEFAULT NULL,
  `case` varchar(50) DEFAULT NULL,
  `death` varchar(50) DEFAULT NULL,
  `updated` varchar(50) DEFAULT NULL,
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;