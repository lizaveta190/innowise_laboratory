-- 1. Create tables
CREATE TABLE IF NOT EXISTS Students (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	full_name TEXT NOT NULL,
	birth_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Grades (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	student_id INTEGER NOT NULL,
	subject TEXT NOT NULL,
	grade INTEGER NOT NULL CHECK(grade >= 1 AND grade <= 100),
	FOREIGN KEY (student_id) REFERENCES students (id)
);

-- 2. Insert data
INSERT INTO students (full_name, birth_year) VALUES
    ("Alice Johnson", 2005),
    ("Brian Smith", 2004),
    ("Carla Reyes", 2006),
    ("Daniel Kim", 2005),
    ("Eva Thompson", 2003),
    ("Felix Nguyen", 2007),
    ("Grace Patel", 2005),
    ("Henry Lopez", 2004),
    ("Isabella Martinez", 2006);

INSERT INTO grades (student_id, subject, grade) VALUES
    (1, 'Math', 88),
    (1, 'English', 92),
    (1, 'Science', 85),
    (2, 'Math', 75),
    (2, 'History', 83),
    (2, 'English', 79),
    (3, 'Science', 95),
    (3, 'Math', 91),
    (3, 'Art', 89),
    (4, 'Math', 84),
    (4, 'Science', 88),
    (4, 'Physical Education', 93),
    (5, 'English', 90),
    (5, 'History', 85),
    (5, 'Math', 88),
    (6, 'Science', 72),
    (6, 'Math', 78),
    (6, 'English', 81),
    (7, 'Art', 94),
    (7, 'Science', 87),
    (7, 'Math', 90),
    (8, 'History', 77),
    (8, 'Math', 83),
    (8, 'Science', 80),
    (9, 'English', 96),
    (9, 'Math', 89),
    (9, 'Art', 92);

-- 3. Find all grades for a specific student (Alice Johnson)
SELECT grades.subject, grades.grade FROM Students 
JOIN Grades ON students.id = grades.student_id 
WHERE students.full_name = 'Alice Johnson';

-- 4. Calculate the average grade per student
SELECT students.full_name, AVG(grades.grade) AS average_grade 
FROM Students
JOIN Grades ON students.id = grades.student_id
GROUP BY students.full_name;

-- 5. List all students born after 2004
SELECT full_name 
FROM Students 
WHERE birth_year > 2004;

-- 6. Create a query that lists all subjects and their average grades
SELECT subject, AVG(grade)
FROM Grades
GROUP BY subject;

--7. Find the top 3 students with the highest average grades
SELECT students.full_name, AVG(grades.grade) AS average_grade 
FROM Students
JOIN Grades ON students.id = grades.student_id
GROUP BY students.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- 8. Show all students who have scored below 80 in any subject
SELECT DISTINCT students.full_name 
FROM Students 
JOIN Grades ON students.id = grades.student_id 
WHERE grade < 80;