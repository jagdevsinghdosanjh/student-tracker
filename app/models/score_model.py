# score_model.py

from datetime import datetime
from bson import ObjectId

class Score:
    def __init__(self, student_id, subject, marks_obtained, total_marks, exam_date, created_at=None, updated_at=None, _id=None):
        self.id = str(_id) if _id else None
        self.student_id = student_id  # Should already be ObjectId
        self.subject = subject
        self.marks_obtained = marks_obtained
        self.total_marks = total_marks
        self.exam_date = exam_date
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": ObjectId(self.id) if self.id else None,
            "student_id": ObjectId(self.student_id),
            "subject": self.subject,
            "marks_obtained": self.marks_obtained,
            "total_marks": self.total_marks,
            "exam_date": self.exam_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_dict(data):
        return Score(
            student_id=data["student_id"],
            subject=data["subject"],
            marks_obtained=data["marks_obtained"],
            total_marks=data["total_marks"],
            exam_date=data["exam_date"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            _id=data.get("_id")
        )
