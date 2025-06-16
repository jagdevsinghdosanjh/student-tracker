# student_model.py

from bson import ObjectId

class Student:
    def __init__(self, name, roll_no, email, _id=None):
        self.id = str(_id) if _id else None
        self.name = name
        self.roll_no = roll_no
        self.email = email

    def to_dict(self):
        return {
            "full_name": self.name,
            "roll_number": self.roll_no, # Assuming roll_no is used as roll_number
            "class_name": self.class_name,  # Assuming roll_no is used as class_name   
            "date_of_birth": None,  # Placeholder, as date_of_birth is not in this model
            "guardian_contact": None,  # Placeholder, as guardian_contact is not in this model
            "_id": ObjectId(self.id) if self.id else None,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        return Student(
            name=data.get("name"),  # Assuming name is used as full_name
            oll_no=data.get("roll_no"), # Assuming roll_no is used as roll_number   
            class_name=data.get("class_name"),  # Assuming class_name is used as class_name
            date_of_birth=data.get("date_of_birth"),  # Placeholder, as date_of_birth is not in this model
            guardian_contact=data.get("guardian_contact"),  # Placeholder, as guardian_contact is not in this model 
            email=data.get("email"),
            _id=data.get("_id")
        )
