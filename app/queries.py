"""Database queries and reporting utilities."""
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

def generate_dynamic_pivot_sql(start_date: datetime, end_date: datetime, session: Session):
    """
    Generate a dynamic SQL query that produces a custom pivot-style report of time entries.

    The query:
      - Builds a date series with 1 day interval.
      - Collects all time entries for that period, grouped by day.
      - Dynamically generates one column per distinct project name, showing the
        total hours logged for that project on each day.
      - Includes a "description" column aggregating all distinct entry descriptions
        for a given day.
      - Includes a "total_hours" column with the total hours for that day across
        all projects.
    """

    # Get all distinct project names from time_entries within date range
    project_names = session.execute(text("""
        SELECT DISTINCT p.name
        FROM time_entries t
        JOIN projects p ON p.id = t.project_id
        WHERE t.start >= :start_date AND t.start < :end_date
    """), {"start_date": start_date, "end_date": end_date}).scalars().all()

    # If no projects are found, return None
    if not project_names:
        return None, None

    # Generate dynamic SQL for project columns
    project_columns = ",\n".join([
        (
            f" SUM(CASE WHEN p.name = :p_{i} "
            f"then round(t.duration/3600.0, 2) else null END) AS \"{name}\""
        )
        for i, name in enumerate(project_names)
    ])


    # Generate the final SQL query
    sql = f"""
        WITH date_series AS (
            SELECT generate_series(DATE :start_date, DATE :end_date - interval '1 day', interval '1 day')::date AS day
        ),
        entry_data AS (
            SELECT
                t.start::date AS day,
                t.description,
                t.duration,
                p.name AS project_name
            FROM time_entries t
            JOIN projects p ON p.id = t.project_id
            WHERE t.start >= :start_date AND t.start < :end_date
        )
        SELECT
            ds.day AS date,
            (
                SELECT concat('"', string_agg(distinct e.description, ', ' ORDER BY e.description), '"')
                FROM entry_data e
                WHERE e.day = ds.day
            ) AS description,
            ROUND(SUM(t.duration)/3600.0, 2) AS total_hours,
        {project_columns}
        FROM date_series ds
        LEFT JOIN entry_data t ON t.day = ds.day
        LEFT JOIN projects p ON p.name = t.project_name
        GROUP BY ds.day
        ORDER BY ds.day;
    """

    # Bind parameters
    params = {
        "start_date": start_date,
        "end_date": end_date,
    }
    for i, name in enumerate(project_names):
        params[f"p_{i}"] = name

    return sql, params
