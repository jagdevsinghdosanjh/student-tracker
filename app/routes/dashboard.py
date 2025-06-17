from flask import render_template, Blueprint

score_bp = Blueprint('score', __name__)

@score_bp.route('/')
def dashboard():
    return render_template('dashboard.html')
