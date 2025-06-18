# app/utils/pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_student_report(student, scores):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, height - 50, f"Progress Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 100, f"Student Name: {student['full_name']}")
    pdf.drawString(50, height - 120, f"Class: {student.get('class_name', 'N/A')}")

    y = height - 160
    total_obtained, total_max = 0, 0

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Subject")
    pdf.drawString(200, y, "Marks Obtained")
    pdf.drawString(350, y, "Total Marks")
    pdf.drawString(480, y, "Percentage")
    y -= 20

    pdf.setFont("Helvetica", 11)
    for score in scores:
        percent = (score['marks_obtained'] / score['total_marks']) * 100
        pdf.drawString(50, y, score['subject'])
        pdf.drawString(200, y, str(score['marks_obtained']))
        pdf.drawString(350, y, str(score['total_marks']))
        pdf.drawString(480, y, f"{percent:.2f}%")
        total_obtained += score['marks_obtained']
        total_max += score['total_marks']
        y -= 20

    # Summary stats
    if y < 120: pdf.showPage(); y = height - 100
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y - 10, "Total:")
    pdf.drawString(200, y - 10, str(total_obtained))
    pdf.drawString(350, y - 10, str(total_max))
    overall_percent = (total_obtained / total_max) * 100 if total_max > 0 else 0
    pdf.drawString(480, y - 10, f"{overall_percent:.2f}%")
    
    # Optional remarks
    y -= 50
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Teacher's Remark:")
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawString(50, y - 20, "Keep up the good work and aim even higher!")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer


# def generate_student_report(student, scores):
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=A4)
#     width, height = A4

#     # Header
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(50, height - 50, f"Progress Report: {student['full_name']}")
#     c.setFont("Helvetica", 12)
#     c.drawString(50, height - 80, f"Class: {student['class_name']} | Roll No: {student['roll_number']}")
#     c.drawString(50, height - 100, f"Date of Birth: {student['date_of_birth']}")

#     # Table Header
#     y = height - 140
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(50, y, "Subject")
#     c.drawString(200, y, "Marks Obtained")
#     c.drawString(350, y, "Total Marks")
#     c.drawString(470, y, "Exam Date")

#     # Table Rows
#     c.setFont("Helvetica", 12)
#     for score in scores:
#         y -= 20
#         c.drawString(50, y, score["subject"])
#         c.drawString(200, y, str(score["marks_obtained"]))
#         c.drawString(350, y, str(score["total_marks"]))
#         c.drawString(470, y, score["exam_date"])

#     c.showPage()
#     c.save()
#     buffer.seek(0)
#     return buffer

