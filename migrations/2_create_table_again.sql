CREATE TABLE `locations` (
    `location_no` CHAR(4) NOT NULL,
    `location_name` VARCHAR(40) NOT NULL,
    PRIMARY KEY (`location_no`),
    UNIQUE KEY `location_name` (`location_name`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_0900_AI_CI;
