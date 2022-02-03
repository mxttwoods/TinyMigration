CREATE TABLE `departments` (
    `dept_no` CHAR(4) NOT NULL,
    `dept_name` VARCHAR(40) NOT NULL,
    PRIMARY KEY (`dept_no`),
    UNIQUE KEY `dept_name` (`dept_name`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_0900_AI_CI;
