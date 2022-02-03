CREATE TABLE `dept_emp` (
    `emp_no` INT NOT NULL,
    `dept_no` CHAR(4) NOT NULL,
    `from_date` DATE NOT NULL,
    `to_date` DATE NOT NULL,
    PRIMARY KEY (`emp_no` , `dept_no`),
    KEY `dept_no` (`dept_no`),
    CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`)
        REFERENCES `employees` (`emp_no`)
        ON DELETE CASCADE,
    CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`)
        REFERENCES `departments` (`dept_no`)
        ON DELETE CASCADE
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_0900_AI_CI;
