
SET NAMES utf8mb4;

-- ---------- 1. TÀI KHOẢN ----------
CREATE TABLE account (
    account_id  VARCHAR(20)  NOT NULL,
    username    VARCHAR(50)  NOT NULL,
    password    VARCHAR(255) NOT NULL,          -- lưu mật khẩu đã băm (hash)
    role        VARCHAR(20)  NOT NULL,          -- student / lecturer / admin / parent
    status      VARCHAR(20)  NOT NULL DEFAULT 'active',
    PRIMARY KEY (account_id),
    UNIQUE KEY uq_account_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 2. KHOA, NGÀNH, KHÓA ----------
CREATE TABLE faculty (
    faculty_id   VARCHAR(20)  NOT NULL,
    faculty_name VARCHAR(150) NOT NULL,
    PRIMARY KEY (faculty_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE major (
    major_id       VARCHAR(20)  NOT NULL,
    major_name     VARCHAR(150) NOT NULL,
         VARCHAR(20)  NOT NULL,
    duration_years DECIMAL(3,1) DEFAULT NULL,
    PRIMARY KEY (major_id),
    CONSTRAINT fk_major_faculty FOREIGN KEY (faculty_id) REFERENCES faculty (faculty_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE cohort (
    cohort_id   VARCHAR(20)  NOT NULL,
    cohort_name VARCHAR(100) NOT NULL,
    start_year  INT          DEFAULT NULL,
    status      VARCHAR(20)  NOT NULL DEFAULT 'active',
    PRIMARY KEY (cohort_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 3. GIẢNG VIÊN ----------
CREATE TABLE lecturer (
    lecturer_id   VARCHAR(20)  NOT NULL,
    name          VARCHAR(100) NOT NULL,
    phone         VARCHAR(20)  DEFAULT NULL,
    email         VARCHAR(255) DEFAULT NULL,
    account_id    VARCHAR(20)  NOT NULL,
    faculty_id    VARCHAR(20)  DEFAULT NULL,
    date_of_birth DATE         DEFAULT NULL,
    gender        VARCHAR(10)  DEFAULT NULL,
    degree        VARCHAR(50)  DEFAULT NULL,
    PRIMARY KEY (lecturer_id),
    UNIQUE KEY uq_lecturer_account (account_id),
    CONSTRAINT fk_lecturer_account FOREIGN KEY (account_id) REFERENCES account (account_id),
    CONSTRAINT fk_lecturer_faculty FOREIGN KEY (faculty_id) REFERENCES faculty (faculty_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 4. LỚP HÀNH CHÍNH ----------
CREATE TABLE administrative_class (
    class_id   VARCHAR(20)  NOT NULL,
    class_name VARCHAR(100) NOT NULL,
    status     VARCHAR(20)  NOT NULL DEFAULT 'active',
    cohort_id  VARCHAR(20)  NOT NULL,
    major_id   VARCHAR(20)  NOT NULL,
    advisor_id VARCHAR(20)  DEFAULT NULL,       -- giảng viên cố vấn
    PRIMARY KEY (class_id),
    CONSTRAINT fk_class_cohort  FOREIGN KEY (cohort_id)  REFERENCES cohort (cohort_id),
    CONSTRAINT fk_class_major   FOREIGN KEY (major_id)   REFERENCES major (major_id),
    CONSTRAINT fk_class_advisor FOREIGN KEY (advisor_id) REFERENCES lecturer (lecturer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 5. SINH VIÊN, PHỤ HUYNH ----------
CREATE TABLE student (
    student_id     VARCHAR(20)  NOT NULL,
    name           VARCHAR(100) NOT NULL,
    phone          VARCHAR(20)  DEFAULT NULL,
    email          VARCHAR(255) DEFAULT NULL,
    account_id     VARCHAR(20)  NOT NULL,
    admin_class_id VARCHAR(20)  DEFAULT NULL,
    date_of_birth  DATE         DEFAULT NULL,
    gender         VARCHAR(10)  DEFAULT NULL,
    status         VARCHAR(20)  NOT NULL DEFAULT 'active',
    PRIMARY KEY (student_id),
    UNIQUE KEY uq_student_account (account_id),
    CONSTRAINT fk_student_account FOREIGN KEY (account_id)     REFERENCES account (account_id),
    CONSTRAINT fk_student_class   FOREIGN KEY (admin_class_id) REFERENCES administrative_class (class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE parent (
    parent_id  VARCHAR(20)  NOT NULL,
    name       VARCHAR(100) NOT NULL,
    phone      VARCHAR(20)  DEFAULT NULL,
    email      VARCHAR(255) DEFAULT NULL,
    account_id VARCHAR(20)  DEFAULT NULL,
    PRIMARY KEY (parent_id),
    CONSTRAINT fk_parent_account FOREIGN KEY (account_id) REFERENCES account (account_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE parent_student (
    parent_id  VARCHAR(20) NOT NULL,
    student_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (parent_id, student_id),
    CONSTRAINT fk_ps_parent  FOREIGN KEY (parent_id)  REFERENCES parent (parent_id)   ON DELETE CASCADE,
    CONSTRAINT fk_ps_student FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 6. DỮ LIỆU SINH TRẮC HỌC ----------
CREATE TABLE fingerprint_data (
    fingerprint_id VARCHAR(20) NOT NULL,
    student_id     VARCHAR(20) NOT NULL,
    data           LONGTEXT    NOT NULL,        -- mẫu vân tay đã mã hóa
    PRIMARY KEY (fingerprint_id),
    CONSTRAINT fk_fp_student FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE face_data (
    face_id    VARCHAR(20) NOT NULL,
    student_id VARCHAR(20) NOT NULL,
    data       LONGTEXT    NOT NULL,            -- vector embedding FaceNet (VD: chuỗi JSON 128 số)
    PRIMARY KEY (face_id),
    CONSTRAINT fk_face_student FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 7. MÔN HỌC, CHƯƠNG TRÌNH ĐÀO TẠO ----------
CREATE TABLE subject (
    subject_id   VARCHAR(20)  NOT NULL,
    subject_name VARCHAR(150) NOT NULL,
    credits      INT          NOT NULL,
    PRIMARY KEY (subject_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE curriculum (
    curriculum_id   VARCHAR(20)  NOT NULL,
    curriculum_name VARCHAR(150) NOT NULL,
    total_credits   INT          DEFAULT NULL,
    major_id        VARCHAR(20)  NOT NULL,
    cohort_id       VARCHAR(20)  NOT NULL,
    PRIMARY KEY (curriculum_id),
    CONSTRAINT fk_curr_major  FOREIGN KEY (major_id)  REFERENCES major (major_id),
    CONSTRAINT fk_curr_cohort FOREIGN KEY (cohort_id) REFERENCES cohort (cohort_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE curriculum_subject (
    curriculum_id         VARCHAR(20) NOT NULL,
    subject_id            VARCHAR(20) NOT NULL,
    semester_no           INT         DEFAULT NULL,
    subject_type          VARCHAR(30) DEFAULT NULL,   -- bắt buộc / tự chọn
    prerequisite_subject_id VARCHAR(20) DEFAULT NULL, -- môn tiên quyết
    PRIMARY KEY (curriculum_id, subject_id),
    CONSTRAINT fk_cs_curriculum FOREIGN KEY (curriculum_id) REFERENCES curriculum (curriculum_id) ON DELETE CASCADE,
    CONSTRAINT fk_cs_subject    FOREIGN KEY (subject_id)    REFERENCES subject (subject_id),
    CONSTRAINT fk_cs_prereq     FOREIGN KEY (prerequisite_subject_id) REFERENCES subject (subject_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 8. PHÒNG HỌC, THIẾT BỊ ----------
CREATE TABLE classroom (
    room_id   INT          NOT NULL AUTO_INCREMENT,
    room_name VARCHAR(50)  NOT NULL,
    status    VARCHAR(20)  NOT NULL DEFAULT 'active',
    capacity  INT          DEFAULT NULL,
    building  VARCHAR(50)  DEFAULT NULL,
    room_type VARCHAR(30)  DEFAULT NULL,
    PRIMARY KEY (room_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE equipment (
    equipment_id   VARCHAR(20)  NOT NULL,
    equipment_name VARCHAR(100) NOT NULL,
    status         VARCHAR(20)  NOT NULL DEFAULT 'active',
    equipment_type VARCHAR(50)  DEFAULT NULL,   -- camera / máy quét vân tay...
    serial_number  VARCHAR(100) DEFAULT NULL,
    room_id        INT          DEFAULT NULL,
    PRIMARY KEY (equipment_id),
    CONSTRAINT fk_equip_room FOREIGN KEY (room_id) REFERENCES classroom (room_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 9. LỚP HỌC PHẦN ----------
CREATE TABLE course_section (
    course_section_id   VARCHAR(20)  NOT NULL,
    course_section_name VARCHAR(150) NOT NULL,
    `time`              TIME         DEFAULT NULL,
    subject_id          VARCHAR(20)  NOT NULL,
    lecturer_id         VARCHAR(20)  DEFAULT NULL,
    semester            DATE         DEFAULT NULL,
    PRIMARY KEY (course_section_id),
    CONSTRAINT fk_csec_subject  FOREIGN KEY (subject_id)  REFERENCES subject (subject_id),
    CONSTRAINT fk_csec_lecturer FOREIGN KEY (lecturer_id) REFERENCES lecturer (lecturer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE student_course_section (
    student_id        VARCHAR(20) NOT NULL,
    course_section_id VARCHAR(20) NOT NULL,
    enrollment_date   DATE        DEFAULT NULL,
    PRIMARY KEY (student_id, course_section_id),
    CONSTRAINT fk_scs_student FOREIGN KEY (student_id)        REFERENCES student (student_id)               ON DELETE CASCADE,
    CONSTRAINT fk_scs_section FOREIGN KEY (course_section_id) REFERENCES course_section (course_section_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 10. BUỔI HỌC ----------
CREATE TABLE session (
    session_id        VARCHAR(20) NOT NULL,
    session_date      DATE        NOT NULL,
    start_time        TIME        NOT NULL,
    end_time          TIME        NOT NULL,
    status            VARCHAR(20) NOT NULL DEFAULT 'scheduled',
    course_section_id VARCHAR(20) NOT NULL,
    room_id           INT         DEFAULT NULL,
    PRIMARY KEY (session_id),
    CONSTRAINT fk_session_section FOREIGN KEY (course_section_id) REFERENCES course_section (course_section_id),
    CONSTRAINT fk_session_room    FOREIGN KEY (room_id)           REFERENCES classroom (room_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 11. ĐIỂM DANH ----------
CREATE TABLE attendance (
    attendance_id     VARCHAR(20) NOT NULL,
    attendance_time   DATETIME    DEFAULT NULL,
    attendance_method VARCHAR(20) DEFAULT NULL,   -- face / fingerprint / manual
    attendance_status VARCHAR(20) NOT NULL,       -- present / late / absent
    editor_lecturer_id VARCHAR(20) DEFAULT NULL,  -- giảng viên chỉnh sửa thủ công
    student_id        VARCHAR(20) NOT NULL,
    session_id        VARCHAR(20) NOT NULL,
    PRIMARY KEY (attendance_id),
    UNIQUE KEY uq_attendance_student_session (student_id, session_id),
    CONSTRAINT fk_att_editor  FOREIGN KEY (editor_lecturer_id) REFERENCES lecturer (lecturer_id),
    CONSTRAINT fk_att_student FOREIGN KEY (student_id)         REFERENCES student (student_id),
    CONSTRAINT fk_att_session FOREIGN KEY (session_id)         REFERENCES session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 12. ĐƠN XIN NGHỈ / KHIẾU NẠI ----------
CREATE TABLE request (
    request_id  VARCHAR(20)  NOT NULL,
    sent_time   DATETIME     NOT NULL,
    status      VARCHAR(20)  NOT NULL DEFAULT 'pending',
    content     TEXT         DEFAULT NULL,
    review_time DATETIME     DEFAULT NULL,
    student_id  VARCHAR(20)  NOT NULL,
    session_id  VARCHAR(20)  DEFAULT NULL,
    attachment  VARCHAR(255) DEFAULT NULL,        -- đường dẫn file minh chứng
    PRIMARY KEY (request_id),
    CONSTRAINT fk_req_student FOREIGN KEY (student_id) REFERENCES student (student_id),
    CONSTRAINT fk_req_session FOREIGN KEY (session_id) REFERENCES session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 13. CẤU HÌNH ĐIỂM DANH ----------
CREATE TABLE attendance_config (
    config_id               VARCHAR(20)  NOT NULL,
    started_time            TIME         DEFAULT NULL,
    last_updated_time       TIME         DEFAULT NULL,
    late_threshold_minutes  INT          DEFAULT NULL,
    absent_threshold_minutes INT         DEFAULT NULL,
    max_absence_rate        DECIMAL(5,2) DEFAULT NULL,
    updated_by_account_id   VARCHAR(20)  DEFAULT NULL,
    course_section_id       VARCHAR(20)  DEFAULT NULL,
    PRIMARY KEY (config_id),
    CONSTRAINT fk_cfg_account FOREIGN KEY (updated_by_account_id) REFERENCES account (account_id),
    CONSTRAINT fk_cfg_section FOREIGN KEY (course_section_id)     REFERENCES course_section (course_section_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- 14. THÔNG BÁO ----------
CREATE TABLE notification (
    notification_id      VARCHAR(20) NOT NULL,
    created_time         DATETIME    NOT NULL,
    content              TEXT        NOT NULL,
    recipient_account_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (notification_id),
    CONSTRAINT fk_notif_account FOREIGN KEY (recipient_account_id) REFERENCES account (account_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
