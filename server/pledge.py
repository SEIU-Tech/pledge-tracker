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
    # Get the data from the form
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    if not first_name or not last_name:
        flash("Both first and last name are required!")
        return redirect(url_for("pledge.index"))

    # Create the database connection
    db = get_db()

    try:
        # Insert the pledge into the database
        db.execute(
            "INSERT INTO pledges (first_name, last_name) VALUES (?, ?)",
            (first_name, last_name),
        )
        db.commit()
        flash(f"Thank you, {first_name}! Your strike pledge has been recorded. Share this page with your coworkers!")
    except Exception as e:
        db.rollback()
        flash("There was an error recording your pledge. Please try again.")
        print("PROBLEM: ", e)
    finally:
        db.close()

    return redirect(url_for("pledge.index"))


@bp.route("/pledges")
def view_pledges():
    db = get_db()
    pledges = db.execute(
        "SELECT id, first_name, last_name, created_at FROM pledges ORDER BY created_at DESC"
    ).fetchall()
    db.close()
    return render_template("pledge/view_pledges.html", pledges=pledges)
