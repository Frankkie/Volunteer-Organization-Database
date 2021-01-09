DROP TABLE IF EXISTS `Contributes to Event`;
DROP TABLE IF EXISTS `Participates In`;
DROP TABLE IF EXISTS `Purchase`;
DROP TABLE IF EXISTS `Contribution`;
DROP TABLE IF EXISTS `Has Contact`;
DROP TABLE IF EXISTS `Works on`;
DROP TABLE IF EXISTS `Project`;
DROP TABLE IF EXISTS `Attends`;
DROP TABLE IF EXISTS `Participant`;
DROP TABLE IF EXISTS `Heads`;
DROP TABLE IF EXISTS `Supervises`;
DROP TABLE IF EXISTS `Event`;
DROP TABLE IF EXISTS `Team`;
DROP TABLE IF EXISTS `Member`;
DROP TABLE IF EXISTS `Contact`;
DROP TABLE IF EXISTS `University Department`;
DROP TABLE IF EXISTS `Field`;
--
-- DROP TABLE IF EXISTS ``;
--


CREATE TABLE `Member` (
	`Id` INT(4) NOT NULL AUTO_INCREMENT,
	`First Name` varchar(32) NOT NULL,
	`Last Name` varchar(32) NOT NULL,
	`Email` varchar(64) NOT NULL,
	`Phone` INT(8),
	`IEEE Number` INT(4) UNIQUE,
	`Activity Status` BINARY NOT NULL DEFAULT '0',
	`Training Date` DATE,
	`Generation` varchar(32),
	`Registration Date` DATETIME NOT NULL,
	`Deletion Date` DATETIME,
	`Studies at` INT NOT NULL,
	`Univ Grade` varchar(32) NOT NULL,
	`Reg Year to Univ` DATE NOT NULL,
	PRIMARY KEY (`Id`)
);

CREATE TABLE `Team` (
	`Team Id` INT NOT NULL AUTO_INCREMENT,
	`Team Name` varchar(255) NOT NULL,
	`Team Type` varchar(64) NOT NULL,
	`IEEE Code` varchar(64),
	`Field` INT NOT NULL,
	PRIMARY KEY (`Team Id`)
);

CREATE TABLE `Participates In` (
	`Member Id` INT(4) NOT NULL,
	`Team Id` INT NOT NULL,
	`Title` varchar(64) NOT NULL DEFAULT 'Member',
	`Start Date` DATE NOT NULL,
	`End Date` DATE,
	PRIMARY KEY (`Member Id`,`Team Id`)
);

CREATE TABLE `Supervises` (
	`Member Id` INT(4) NOT NULL,
	`Team Id` INT NOT NULL,
	`Title` varchar(64) NOT NULL,
	`Start Date` DATE NOT NULL,
	`End Date` DATE,
	PRIMARY KEY (`Member Id`,`Team Id`)
);

CREATE TABLE `Heads` (
	`Member Id` INT(4) NOT NULL,
	`Team Id` INT NOT NULL,
	`Title` varchar(64) NOT NULL,
	`Start Date` DATE NOT NULL,
	`End Date` DATE,
	PRIMARY KEY (`Member Id`,`Team Id`)
);

CREATE TABLE `Works on` (
	`Team Id` INT NOT NULL,
	`Project Id` INT(4) NOT NULL,
	PRIMARY KEY (`Team Id`,`Project Id`)
);

CREATE TABLE `Event` (
	`Event Title` varchar(255) NOT NULL,
	`Event Date` DATETIME NOT NULL,
	`Organized By` INT NOT NULL,
	`Event Type` varchar(255) NOT NULL,
	`Place` varchar(255) NOT NULL,
	PRIMARY KEY (`Event Title`,`Event Date`)
);

CREATE TABLE `Attends` (
	`Participant Email` varchar(64) NOT NULL,
	`Event Title` varchar(255) NOT NULL,
	`Event Date` DATETIME NOT NULL,
	PRIMARY KEY (`Participant Email`,`Event Title`,`Event Date`)
);

CREATE TABLE `Participant` (
	`Email` varchar(64) NOT NULL,
	`First Name` varchar(64) NOT NULL,
	`Last Name` varchar(64) NOT NULL,
	`Subscribed` BINARY NOT NULL DEFAULT '0',
	`Interested in Membership` BINARY NOT NULL DEFAULT '0',
	PRIMARY KEY (`Email`)
);

CREATE TABLE `University Department` (
	`Department Id` INT NOT NULL AUTO_INCREMENT,
	`Department Name` varchar(255) NOT NULL,
	PRIMARY KEY (`Department Id`)
);

CREATE TABLE `Has Contact` (
	`Team Id` INT NOT NULL,
	`Contact Id` INT(4) NOT NULL,
	PRIMARY KEY (`Team Id`,`Contact Id`)
);

CREATE TABLE `Contact` (
	`Contact Id` INT(4) NOT NULL AUTO_INCREMENT,
	`Contact Email` varchar(255) NOT NULL,
	`Phone` INT(8),
	`First Name` varchar(32) NOT NULL,
	`Last Name` varchar(32) NOT NULL,
	`Address` varchar(255) NOT NULL,
	`Date Created` TIMESTAMP NOT NULL,
	`IEEE Position` varchar(255),
	`Field` INT NOT NULL,
	`Uni Department` INT,
	PRIMARY KEY (`Contact Id`)
);

CREATE TABLE `Contributes to Event` (
	`Event Title` varchar(255) NOT NULL,
	`Event Date` DATETIME NOT NULL,
	`Contact Id` INT(4) NOT NULL,
	PRIMARY KEY (`Event Title`,`Event Date`,`Contact Id`)
);

CREATE TABLE `Project` (
	`Project Id` INT(4) NOT NULL AUTO_INCREMENT,
	`Project Title` varchar(255) NOT NULL,
	`Start Date` DATE NOT NULL,
	`End Date` DATE,
	PRIMARY KEY (`Project Id`)
);

CREATE TABLE `Field` (
	`Field Id` INT NOT NULL AUTO_INCREMENT,
	`Field Name` varchar(255) NOT NULL,
	PRIMARY KEY (`Field Id`,`Field Name`)
);

CREATE TABLE `Purchase` (
	`Purchase Id` INT(4) NOT NULL AUTO_INCREMENT,
	`Purchased by` INT(4),
	`Date` DATETIME NOT NULL,
	`Type` varchar(255) NOT NULL,
	`Cost` INT(4) NOT NULL,
	`Stored In` varchar(255),
	PRIMARY KEY (`Purchase Id`)
);

CREATE TABLE `Contribution` (
	`Contribution Id` INT(4) NOT NULL AUTO_INCREMENT,
	`Given By` INT(4) NOT NULL,
	`Date` DATETIME NOT NULL,
	`Type` varchar(255) NOT NULL,
	`Package` varchar(255) NOT NULL,
	`Stored In` varchar(255) NOT NULL,
	PRIMARY KEY (`Contribution Id`)
);


--
-- Additions
--

ALTER TABLE `Event` ADD INDEX `Event_in0` (`Event Date`);

--
-- Additions
--



ALTER TABLE `Member` ADD CONSTRAINT `Member_fk0` FOREIGN KEY (`Studies at`) REFERENCES `University Department`(`Department Id`);

ALTER TABLE `Team` ADD CONSTRAINT `Team_fk0` FOREIGN KEY (`Field`) REFERENCES `Field`(`Field Id`);

ALTER TABLE `Participates In` ADD CONSTRAINT `Participates In_fk0` FOREIGN KEY (`Member Id`) REFERENCES `Member`(`Id`);

ALTER TABLE `Participates In` ADD CONSTRAINT `Participates In_fk1` FOREIGN KEY (`Team Id`) REFERENCES `Team`(`Team Id`);

ALTER TABLE `Supervises` ADD CONSTRAINT `Supervises_fk0` FOREIGN KEY (`Member Id`) REFERENCES `Member`(`Id`);

ALTER TABLE `Supervises` ADD CONSTRAINT `Supervises_fk1` FOREIGN KEY (`Team Id`) REFERENCES `Team`(`Team Id`);

ALTER TABLE `Heads` ADD CONSTRAINT `Heads_fk0` FOREIGN KEY (`Member Id`) REFERENCES `Member`(`Id`);

ALTER TABLE `Heads` ADD CONSTRAINT `Heads_fk1` FOREIGN KEY (`Team Id`) REFERENCES `Team`(`Team Id`);

ALTER TABLE `Works on` ADD CONSTRAINT `Works on_fk0` FOREIGN KEY (`Team Id`) REFERENCES `Team`(`Team Id`);

ALTER TABLE `Works on` ADD CONSTRAINT `Works on_fk1` FOREIGN KEY (`Project Id`) REFERENCES `Project`(`Project Id`);

ALTER TABLE `Event` ADD CONSTRAINT `Event_fk0` FOREIGN KEY (`Organized By`) REFERENCES `Team`(`Team Id`);

ALTER TABLE `Attends` ADD CONSTRAINT `Attends_fk0` FOREIGN KEY (`Participant Email`) REFERENCES `Participant`(`Email`);

ALTER TABLE `Attends` ADD CONSTRAINT `Attends_fk1` FOREIGN KEY (`Event Title`) REFERENCES `Event`(`Event Title`);

ALTER TABLE `Attends` ADD CONSTRAINT `Attends_fk2` FOREIGN KEY (`Event Date`) REFERENCES `Event`(`Event Date`);

ALTER TABLE `Has Contact` ADD CONSTRAINT `Has Contact_fk0` FOREIGN KEY (`Team Id`) REFERENCES `Team`(`Team Id`);

ALTER TABLE `Has Contact` ADD CONSTRAINT `Has Contact_fk1` FOREIGN KEY (`Contact Id`) REFERENCES `Contact`(`Contact Id`);

ALTER TABLE `Contact` ADD CONSTRAINT `Contact_fk0` FOREIGN KEY (`Field`) REFERENCES `Field`(`Field Id`);

ALTER TABLE `Contact` ADD CONSTRAINT `Contact_fk1` FOREIGN KEY (`Uni Department`) REFERENCES `University Department`(`Department Id`);

ALTER TABLE `Contributes to Event` ADD CONSTRAINT `Contributes to Event_fk0` FOREIGN KEY (`Event Title`) REFERENCES `Event`(`Event Title`);

ALTER TABLE `Contributes to Event` ADD CONSTRAINT `Contributes to Event_fk1` FOREIGN KEY (`Event Date`) REFERENCES `Event`(`Event Date`);

ALTER TABLE `Contributes to Event` ADD CONSTRAINT `Contributes to Event_fk2` FOREIGN KEY (`Contact Id`) REFERENCES `Contact`(`Contact Id`);

ALTER TABLE `Purchase` ADD CONSTRAINT `Purchase_fk0` FOREIGN KEY (`Purchased by`) REFERENCES `Contact`(`Contact Id`);

ALTER TABLE `Contribution` ADD CONSTRAINT `Contribution_fk0` FOREIGN KEY (`Given By`) REFERENCES `Contact`(`Contact Id`);

