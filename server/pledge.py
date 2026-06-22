from flask import Blueprint, render_template, request, flash, redirect, url_for

from server.db import get_db

bp = Blueprint("pledge", __name__)


# Render the form
@bp.route("/")
def index():
    return render_template("pledge/index.html")


# Handle the data submission
@bp.route("/submit-pledge", methods=["POST"])
def submit_pledge():
    # get the data from the form
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    if not first_name or not last_name:
        flash("Both first and last name are required!")
        return redirect(url_for("home.index"))

    # TODO: Save to SQLite database here

    flash(f"Thank you, {first_name}! Your strike pledge has been recorded.")

    # Redirect back to the form page after successful submission
    return redirect(url_for("pledge.index"))
