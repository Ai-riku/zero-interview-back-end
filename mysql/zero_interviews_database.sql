DROP DATABASE IF EXISTS `zero_interviews`;
CREATE DATABASE `zero_interviews`;
USE `zero_interviews`;


DROP TABLE IF EXISTS `users` ;
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL,
  `username` VARCHAR(50),
  `firstname` VARCHAR(50),
  `lastname` VARCHAR(50),
  `profile_id` INT,
  `created_at` TIMESTAMP,
  PRIMARY KEY (`id`)
);

INSERT INTO `users` (`id`, `username`, `firstname`, `lastname`, `profile_id`, `created_at`)
VALUES
(1, 'test1', 'Leslie', 'Knope', 44, '2019-09-25'),
(2, 'test2', 'Tom', 'Haverford', 36, '2017-03-04'),
(3, 'test3', 'April', 'Ludgate', 29, '2024-03-27');

DROP TABLE IF EXISTS `profiles` ;
CREATE TABLE IF NOT EXISTS `profiles` (
  `id` INT NOT NULL,
  `profile_type` VARCHAR(50),
  `profile_role` VARCHAR(50),
  `created_at` TIMESTAMP,
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `interviews` ;
CREATE TABLE IF NOT EXISTS `interviews` (
  `id` INT NOT NULL,
  `profile_id` INT,
  `interviews_role` VARCHAR(50),
  `interviews_type` VARCHAR(50),
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `questions` ;
CREATE TABLE IF NOT EXISTS `questions` (
  `id` INT NOT NULL,
  `question` TEXT,
  `question_role` VARCHAR(50),
  `question_type` VARCHAR(50),
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `answers` ;
CREATE TABLE IF NOT EXISTS `answers` (
  `id` INT NOT NULL,
  `profile_id` INT,
  `question_id` INT,
  `answer` TEXT,
  `video_link` VARCHAR(255),
  PRIMARY KEY (`id`)
);