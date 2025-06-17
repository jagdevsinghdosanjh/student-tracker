from flask import Blueprint, request, jsonify, render_template, send_file
from bson.objectid import ObjectId
from datetime import datetime
from app import mongo
from app.utils.auth_utils import token_required
from app.utils.image_handler import save_image, get_image, delete_image
import io

student_bp = Blueprint('students', __name__)

# ▶️ Add a new student
@student_bp.route('/', methods=['POST'])
@token_required
def add_student():
    data = request.form
    photo = request.files.get('photo')

    if not all(k in data for k in ("full_name", "roll_number", "class_name", "date_of_birth", "guardian_contact")):
        return jsonify({"error": "Missing required fields"}), 400

    photo_id = save_image(photo) if photo else None

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

# 📋 Fetch all students
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

# 🖼️ Get student photo by ID
@student_bp.route('/photo/<photo_id>', methods=['GET'])
@token_required 
def get_photo(photo_id):
    binary_data, mime, filename = get_image(photo_id)
    if binary_data:
        return send_file(
            io.BytesIO(binary_data),
            mimetype=mime or 'image/jpeg',
            as_attachment=False,
            download_name=filename or 'photo.jpg'
        )
    else:
        return jsonify({"error": "Photo not found"}), 404
    
# 🗑️ Delete student photo by ID
@student_bp.route('/photo/<photo_id>', methods=['DELETE'])
@token_required
def delete_photo(photo_id):
    if delete_image(photo_id):
        return jsonify({"message": "Photo deleted successfully"}), 200
    else:
        return jsonify({"error": "Photo not found"}), 404   

# 📝 Update student details
@student_bp.route('/<student_id>', methods=['PUT'])
@token_required
def update_student(student_id):
    data = request.form
    photo = request.files.get('photo')

    if not all(k in data for k in ("full_name", "roll_number", "class_name", "date_of_birth", "guardian_contact")):
        return jsonify({"error": "Missing required fields"}), 400

    student_doc = {
        "full_name": data['full_name'],
        "roll_number": data['roll_number'],
        "class_name": data['class_name'],
        "date_of_birth": data['date_of_birth'],
        "guardian_contact": data['guardian_contact'],
        "updated_at": datetime.utcnow()
    }

    if photo:
        photo_id = save_image(photo)
        student_doc["photo_id"] = photo_id

    result = mongo.db.students.update_one({"_id": ObjectId(student_id)}, {"$set": student_doc})

    if result.matched_count == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student updated successfully"}), 200        

# 🗑️ Delete a student   
@student_bp.route('/<student_id>', methods=['DELETE'])
@token_required
def delete_student(student_id):
    result = mongo.db.students.delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"}), 200    

# ▶️ View student
@student_bp.route('/<student_id>', methods=['GET'])
@token_required
def view_student(student_id):
    student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    scores = list(mongo.db.scores.find({"student_id": ObjectId(student_id)}))
    
    return render_template('student_detail.html', student=student, scores=scores)

# ▶️ View student scores
@student_bp.route('/<student_id>/scores', methods=['GET'])
@token_required
def view_student_scores(student_id):
    scores = list(mongo.db.scores.find({"student_id": ObjectId(student_id)}))
    
    if not scores:
        return jsonify({"message": "No scores found for this student"}), 404

    return render_template('student_scores.html', scores=scores)

# ▶️ Add a score for a student
@student_bp.route('/<student_id>/scores', methods=['POST'])
@token_required
def add_student_score(student_id):
    data = request.json

    if not all(k in data for k in ("subject", "score", "date")):
        return jsonify({"error": "Missing required fields"}), 400

    score_doc = {
        "student_id": ObjectId(student_id),
        "subject": data['subject'],
        "score": data['score'],
        "date": data['date'],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = mongo.db.scores.insert_one(score_doc)
    return jsonify({"message": "Score added successfully", "id": str(result.inserted_id)}), 201

# ▶️ Update a student's score
@student_bp.route('/<student_id>/scores/<score_id>', methods=['PUT'])
@token_required
def update_student_score(student_id, score_id):
    data = request.json

    if not all(k in data for k in ("subject", "score", "date")):
        return jsonify({"error": "Missing required fields"}), 400

    score_doc = {
        "subject": data['subject'],
        "score": data['score'],
        "date": data['date'],
        "updated_at": datetime.utcnow()
    }

    result = mongo.db.scores.update_one(
        {"_id": ObjectId(score_id), "student_id": ObjectId(student_id)},
        {"$set": score_doc}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Score not found"}), 404

    return jsonify({"message": "Score updated successfully"}), 200

# ▶️ Delete a student's score
@student_bp.route('/<student_id>/scores/<score_id>', methods=['DELETE'])
@student_bp.route('/<student_id>/scores/<score_id>', methods=['DELETE'])
@token_required
def delete_student_score(student_id, score_id):
    result = mongo.db.scores.delete_one({"_id": ObjectId(score_id), "student_id": ObjectId(student_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Score not found"}), 404

    return jsonify({"message": "Score deleted successfully"}), 200  

score_bp = Blueprint('score', __name__)

@score_bp.route('/')
def dashboard():
    return render_template('dashboard.html')
# Register the blueprint
def register_routes(app):
    app.register_blueprint(student_bp, url_prefix='/students')
    app.register_blueprint(score_bp, url_prefix='/scores')
    
    