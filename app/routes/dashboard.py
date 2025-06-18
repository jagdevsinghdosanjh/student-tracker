# app/routes/dashboard.py

# In dashboard.py
from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# from flask import render_template, Blueprint

# score_bp = Blueprint('score', __name__)

# @score_bp.route('/')
# def dashboard():
#     return render_template('dashboard.html')
