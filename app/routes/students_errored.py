from flask import send_file
import io
from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import mongo
from gridfs import GridFS
from app.utils.auth_utils import token_required
from flask import render_template



student_bp = Blueprint('students', __name__)
fs = GridFS(mongo.db)

@student_bp.route('/', methods=['POST'])
@token_required
def add_student():
    data = request.form
    photo = request.files.get('photo')

    if not all (k in data for k in ("full_name", "roll_number", "class_name", "date_of_birth", "guardian_contact")):
        return jsonify({"error": "Missing required fields"}), 400

    # Save photo to GridFS if uploaded
    photo_id = None
    if photo:
        photo_id = fs.put(photo, filename=photo.filename)

    student_doc = {
        "full_name": data['full_name'],
        "roll_number": data['roll_number'],
        "class_name": data['class_name'],
        "date_of_birth": data['date_of_birth'],
        "guardian_contact": data['guardian_contact'],
        "photo_id": photo_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = mongo.db.students.insert_one(student_doc)
    return jsonify({"message": "Student added successfully", "id": str(result.inserted_id)}), 201
@student_bp.route('/', methods=['GET'])
def get_students():
    students = mongo.db.students.find()
    result = []

    for student in students:
        result.append({
            "id": str(student["_id"]),
            "full_name": student["full_name"],
            "roll_number": student["roll_number"],
            "class_name": student["class_name"],
            "date_of_birth": student["date_of_birth"],
            "guardian_contact": student["guardian_contact"],
            "photo_id": str(student["photo_id"]) if student.get("photo_id") else None,
            "created_at": student["created_at"],
            "updated_at": student["updated_at"]
        })

    return jsonify(result), 200

@student_bp.route('/photo/<photo_id>', methods=['GET'])
def get_photo(photo_id):
    try:
        photo = fs.get(ObjectId(photo_id))
        return send_file(
            io.BytesIO(photo.read()),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name=photo.filename
        )
    except Exception:
        return jsonify({"error": "Photo not found"}), 404

@student_bp.route('/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    update_fields = {
        key: data[key]
        for key in ["full_name", "roll_number", "class_name", "date_of_birth", "guardian_contact"]
        if key in data
    }
    update_fields["updated_at"] = datetime.utcnow()

    result = mongo.db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student updated successfully"}), 200

@student_bp.route('/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Delete photo from GridFS
    photo_id = student.get("photo_id")
    if photo_id:
        fs.delete(ObjectId(photo_id))

    mongo.db.students.delete_one({"_id": ObjectId(student_id)})
    return jsonify({"message": "Student deleted successfully"}), 200


# The following image handler calls are examples and should be used within appropriate routes or functions where 'photo' and 'photo_id' are defined.
# photo_id = save_image(photo)
# binary_data, mime, name = get_image(photo_id)
# delete_image(photo_id)

@student_bp.route('/<student_id>')
@token_required
def view_student(student_id):
    student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
    return render_template('student_detail.html', student=student)

