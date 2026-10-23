
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, Finding
from pathlib import Path

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-before-deployment"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///securevault.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()



@app.route("/")
def dashboard():
    search = request.args.get("search", "").strip()
    severity = request.args.get("severity", "").strip()

    query = Finding.query

    if search:
        query = query.filter(Finding.title.ilike(f"%{search}%"))

    if severity in ["Critical", "High", "Medium", "Low"]:
        query = query.filter_by(severity=severity)
    else:
        severity = ""

    findings = query.order_by(Finding.id.desc()).all()

    counts = {
        "total": Finding.query.count(),
        "critical": Finding.query.filter_by(severity="Critical").count(),
        "high": Finding.query.filter_by(severity="High").count(),
        "medium": Finding.query.filter_by(severity="Medium").count(),
        "low": Finding.query.filter_by(severity="Low").count(),
    }

    return render_template(
        "dashboard.html",
        findings=findings,
        counts=counts,
        search=search,
        severity=severity
    )



@app.route("/add", methods=["GET", "POST"])
def add_finding():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        severity = request.form.get("severity", "")
        description = request.form.get("description", "").strip()
        impact = request.form.get("impact", "").strip()
        remediation = request.form.get("remediation", "").strip()

        if not all([title, severity, description, impact, remediation]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for("add_finding"))

        if severity not in ["Critical", "High", "Medium", "Low"]:
            flash("Invalid severity selected.", "error")
            return redirect(url_for("add_finding"))

        finding = Finding(
            title=title,
            severity=severity,
            description=description,
            impact=impact,
            remediation=remediation
        )

        db.session.add(finding)
        db.session.commit()

        flash("Finding added successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("finding_form.html")

@app.route("/finding/<int:finding_id>")
def finding_detail(finding_id):
    finding = db.session.get(Finding, finding_id)

    if finding is None:
        flash("Finding not found.", "error")
        return redirect(url_for("dashboard"))

    return render_template("finding_detail.html", finding=finding)
@app.route("/finding/<int:finding_id>/status", methods=["POST"])
def update_status(finding_id):
    finding = db.session.get(Finding, finding_id)

    if finding is None:
        flash("Finding not found.", "error")
        return redirect(url_for("dashboard"))

    new_status = request.form.get("status", "")

    if new_status not in ["Open", "In Progress", "Resolved"]:
        flash("Invalid status.", "error")
        return redirect(url_for("dashboard"))

    finding.status = new_status
    db.session.commit()

    flash("Finding status updated.", "success")
    return redirect(url_for("dashboard"))


@app.route("/finding/<int:finding_id>/delete", methods=["POST"])
def delete_finding(finding_id):
    finding = db.session.get(Finding, finding_id)

    if finding is None:
        flash("Finding not found.", "error")
        return redirect(url_for("dashboard"))

    db.session.delete(finding)
    db.session.commit()

    flash("Finding deleted.", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
