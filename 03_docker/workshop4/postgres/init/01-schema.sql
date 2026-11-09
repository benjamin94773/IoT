CREATE SCHEMA IF NOT EXISTS academia;

CREATE TABLE IF NOT EXISTS academia.students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS academia.teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS academia.courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    CONSTRAINT fk_course_teacher
        FOREIGN KEY (teacher_id)
        REFERENCES academia.teachers(id)
);

CREATE TABLE IF NOT EXISTS academia.enrollments (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, course_id),
    CONSTRAINT fk_enrollment_student
        FOREIGN KEY (student_id)
        REFERENCES academia.students(id),
    CONSTRAINT fk_enrollment_course
        FOREIGN KEY (course_id)
        REFERENCES academia.courses(id)
);