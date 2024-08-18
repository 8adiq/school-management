DROP TABLE IF EXISTS Students_1;

-- creating a students table
CREATE TABLE Students_1 (
	student_id SERIAL PRIMARY KEY,
	student_name VARCHAR(50),
	age INT,
	grade INT
);

INSERT INTO students_1 (student_id,student_name,age,grade) VALUES 
(1,'abdul',25,67),
(2,'sani',22,79),
(3,'adama',20,54);

UPDATE students_1 SET age = 19 WHERE student_name = 'adama'; 

-- SELECT MAX(student_id) FROM students_1
ALTER SEQUENCE students_1_student_id_seq RESTART WITH 11;

SELECT * FROM students_1