INSERT INTO academia.students (name, email) VALUES
('Ana', 'ana@example.com'),
('Luis', 'luis@example.com'),
('Marta', 'marta@example.com');

INSERT INTO academia.teachers (name, email) VALUES
('Carlos Perez', 'carlos@example.com'),
('Laura Gomez', 'laura@example.com');

INSERT INTO academia.courses (name, credits, teacher_id) VALUES
('Cloud Computing', 3, 1),
('Internet of Things', 4, 2);

INSERT INTO academia.enrollments (student_id, course_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 2);