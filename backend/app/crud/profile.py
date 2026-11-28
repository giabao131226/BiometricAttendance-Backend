from sqlalchemy import text
from sqlalchemy.orm import Session

STUDENT_SQL = text("""
    SELECT s.student_id AS user_id, s.name, s.phone, s.email,
           s.date_of_birth, s.gender, s.status,
           c.class_id, c.class_name,
           co.cohort_name,
           m.major_id, m.major_name,
           f.faculty_id, f.faculty_name
    FROM student s
    LEFT JOIN administrative_class c ON c.class_id = s.admin_class_id
    LEFT JOIN cohort co ON co.cohort_id = c.cohort_id
    LEFT JOIN major m ON m.major_id = c.major_id
    LEFT JOIN faculty f ON f.faculty_id = m.faculty_id
    WHERE s.account_id = :account_id
""")

LECTURER_SQL = text("""
    SELECT l.lecturer_id AS user_id, l.name, l.phone, l.email,
           l.date_of_birth, l.gender, l.degree,
           a.status,
           f.faculty_id, f.faculty_name
    FROM lecturer l
    JOIN account a ON a.account_id = l.account_id
    LEFT JOIN faculty f ON f.faculty_id = l.faculty_id
    WHERE l.account_id = :account_id
""")


def get_profile(db: Session, account_id: str, role: str):
    if role == "student":
        row = db.execute(STUDENT_SQL, {"account_id": account_id}).mappings().first()
        if not row:
            return None
        profile = dict(row)
        sid = profile["user_id"]
        profile["face_count"] = db.execute(
            text("SELECT COUNT(*) FROM face_data WHERE student_id = :sid"),
            {"sid": sid},
        ).scalar()
        profile["fingerprint_count"] = db.execute(
            text("SELECT COUNT(*) FROM fingerprint_data WHERE student_id = :sid"),
            {"sid": sid},
        ).scalar()
    elif role == "lecturer":
        row = db.execute(LECTURER_SQL, {"account_id": account_id}).mappings().first()
        if not row:
            return None
        profile = dict(row)
    else:
        return None

    profile["role"] = role
    return profile