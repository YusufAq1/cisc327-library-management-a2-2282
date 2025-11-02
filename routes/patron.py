from flask import Blueprint, render_template, request, flash
from services.library_service import get_patron_status_report

patron_bp = Blueprint("patron", __name__, url_prefix="/patron")

@patron_bp.route("/", methods=["GET", "POST"])
def patron_home():
    report = None
    if request.method == "POST":
        patron_id = request.form.get("patron_id")
        report = get_patron_status_report(patron_id)
        if not report["success"]:
            flash(report["message"], "error")
        else:
            flash(report["message"], "success")
    return render_template("patron.html", report=report)