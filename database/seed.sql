USE biometric_attendance;
SET NAMES utf8mb4;

-- 1. FACULTY
INSERT INTO faculty (faculty_id, faculty_name) VALUES
('CNTT', 'Khoa Công nghệ thông tin'),
('KT',   'Khoa Kinh tế'),
('NN',   'Khoa Ngoại ngữ'),
('CK',   'Khoa Cơ khí');

-- 2. MAJOR
INSERT INTO major (major_id, major_name, faculty_id, duration_years) VALUES
('7480201', 'Công nghệ thông tin', 'CNTT', 4.0),
('7480103', 'Kỹ thuật phần mềm',   'CNTT', 4.0),
('7340101', 'Quản trị kinh doanh', 'KT',   4.0),
('7220201', 'Ngôn ngữ Anh',        'NN',   4.0),
('7520103', 'Kỹ thuật cơ khí',     'CK',   4.5);

-- 3. SUBJECT
INSERT INTO subject (subject_id, subject_name, credits) VALUES
('INT1001', 'Nhập môn lập trình', 3),
('INT1003', 'Cơ sở dữ liệu',      3),
('ECO1001', 'Kinh tế vi mô',      2),
('ENG1001', 'Tiếng Anh cơ bản',   2);