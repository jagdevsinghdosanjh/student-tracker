# student_model.py

from bson import ObjectId

class Student:
    def __init__(self, name, roll_no, email, class_name=None, date_of_birth=None, guardian_contact=None, _id=None):
        self.id = str(_id) if _id else None
        self.name = name
        self.roll_no = roll_no
        self.email = email
        self.class_name = class_name
        self.date_of_birth = date_of_birth
        self.guardian_contact = guardian_contact

    def to_dict(self):
        return {
            "full_name": self.name,
            "roll_number": self.roll_no,
            "class_name": self.class_name,
            "date_of_birth": self.date_of_birth,
            "guardian_contact": self.guardian_contact,
            "_id": ObjectId(self.id) if self.id else None,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        return Student(
            name=data.get("full_name"),
            roll_no=data.get("roll_number"),
            email=data.get("email"),
            class_name=data.get("class_name"),
            date_of_birth=data.get("date_of_birth"),
            guardian_contact=data.get("guardian_contact"),
            _id=data.get("_id")
        )
