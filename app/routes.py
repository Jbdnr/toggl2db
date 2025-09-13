"""Routes for the Flask application."""
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from .database import get_db_session
from .queries import generate_dynamic_pivot_sql
from .toggl_import import import_toggl_data

bp = Blueprint("routes", __name__)

@bp.route("/", methods=["GET"])
def report():
    """Render the report page with time entries."""
    today = date.today()
    year = int(request.args.get("year", today.year))
    month = int(request.args.get("month", today.month))

    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    with get_db_session() as session:
        sql, params = generate_dynamic_pivot_sql(start_date, end_date, session)

        if sql is None:
            rows = []
            headers = []
        else:
            result = session.execute(text(sql), params)
            rows = result.fetchall()
            headers = result.keys()

    return render_template("report.html", headers=headers, rows=rows, year=year, month=month)


@bp.route("/import")
def import_data():
    """Import data from Toggl for the specified month and year."""
    today = date.today()
    year = int(request.args.get("year", today.year))
    month = int(request.args.get("month", today.month))

    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    start_date_str = request.args.get("start", start_date)
    end_date_str = request.args.get("end", end_date)

    import_toggl_data(start_date_str, end_date_str)

    return redirect(url_for("routes.report", year=year, month=month))
