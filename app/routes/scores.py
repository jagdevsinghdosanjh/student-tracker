from bson.son import SON
from flask import Blueprint, request, jsonify
from app import mongo
from datetime import datetime
from bson.objectid import ObjectId
from app.utils.auth_utils import token_required
from flask import send_file
from app.utils.pdf_generator import generate_student_report
from flask import render_template

score_bp = Blueprint('scores', __name__)

@score_bp.route('/', methods=['POST'])
@token_required
def add_score():
    data = request.get_json()
    required = ["student_id", "subject", "marks_obtained", "total_marks", "exam_date"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    score = {
        "student_id": ObjectId(data["student_id"]),
        "subject": data["subject"],
        "marks_obtained": int(data["marks_obtained"]),
        "total_marks": int(data["total_marks"]),
        "exam_date": data["exam_date"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    mongo.db.scores.insert_one(score)
    return jsonify({"message": "Score added"}), 201

@score_bp.route('/student/<student_id>', methods=['GET'])
def get_scores_by_student(student_id):
    scores = mongo.db.scores.find({"student_id": ObjectId(student_id)})
    result = []
    for s in scores:
        result.append({
            "subject": s["subject"],
            "marks_obtained": s["marks_obtained"],
            "total_marks": s["total_marks"],
            "exam_date": s["exam_date"]
        })
    return jsonify(result), 200

@score_bp.route('/dashboard/recent', methods=['GET'])
@token_required
def recent_scores():
    scores = mongo.db.scores.find().sort("exam_date", -1).limit(10)
    enriched = []
    for s in scores:
        student = mongo.db.students.find_one({"_id": s["student_id"]})
        enriched.append({
            "studentName": student["full_name"] if student else "Unknown",
            "subject": s["subject"],
            "percentage": round((s["marks_obtained"] / s["total_marks"]) * 100, 2),
            "date": s["exam_date"]
        })
    return jsonify(enriched)

@score_bp.route('/analytics/subject-averages', methods=['GET'])
def subject_averages():
    pipeline = [
        {"$group": {
            "_id": "$subject",
            "average": {"$avg": {"$multiply": [{"$divide": ["$marks_obtained", "$total_marks"]}, 100]}}
        }},
        {"$project": {"subject": "$_id", "average": {"$round": ["$average", 2]}}},
        {"$sort": SON([("subject", 1)])}
    ]
    result = list(mongo.db.scores.aggregate(pipeline))
    return jsonify(result)



@score_bp.route('/report/<student_id>', methods=['GET'])
@token_required
def download_report(student_id):
    student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    scores = list(mongo.db.scores.find({"student_id": ObjectId(student_id)}))
    pdf_buffer = generate_student_report(student, scores)

    filename = f"{student['full_name'].replace(' ', '_')}_Report.pdf"
    return send_file(pdf_buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

@score_bp.route('/dashboard/recent', methods=['GET'])
def get_recent_scores():
    scores = mongo.db.scores.find().sort("exam_date", -1).limit(10)
    result = []
    for s in scores:
        student = mongo.db.students.find_one({"_id": s["student_id"]})
        result.append({
            "studentName": student["full_name"] if student else "Unknown",
            "subject": s["subject"],
            "percentage": round((s["marks_obtained"] / s["total_marks"]) * 100, 2),
            "date": s["exam_date"]
        })
    return jsonify(result)

@score_bp.route('/form', methods=['GET'])
def score_form():
    return render_template('add_score.html')
