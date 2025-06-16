from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_student_report(student, scores):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Progress Report: {student['full_name']}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Class: {student['class_name']} | Roll No: {student['roll_number']}")
    c.drawString(50, height - 100, f"Date of Birth: {student['date_of_birth']}")

    # Table Header
    y = height - 140
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Subject")
    c.drawString(200, y, "Marks Obtained")
    c.drawString(350, y, "Total Marks")
    c.drawString(470, y, "Exam Date")

    # Table Rows
    c.setFont("Helvetica", 12)
    for score in scores:
        y -= 20
        c.drawString(50, y, score["subject"])
        c.drawString(200, y, str(score["marks_obtained"]))
        c.drawString(350, y, str(score["total_marks"]))
        c.drawString(470, y, score["exam_date"])

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
