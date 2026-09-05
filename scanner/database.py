import sqlite3
from datetime import date
from pathlib import Path
from .models import Job

COLUMNS = ["job_id", "title", "company", "location", "deadline", "paid", "cover_letter_required", "source", "source_url", "date_found", "status"]


def connect(path="internships.db"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS internships (
        job_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT NOT NULL,
        deadline TEXT NOT NULL,
        paid TEXT NOT NULL CHECK(paid IN ('yes','no','unknown')),
        cover_letter_required TEXT NOT NULL CHECK(cover_letter_required IN ('yes','no','unknown')),
        source TEXT NOT NULL,
        source_url TEXT NOT NULL,
        date_found TEXT NOT NULL,
        status TEXT NOT NULL
    )""")
    conn.commit()
    return conn


def insert_job(conn, job: Job) -> bool:
    values = (job.job_id, job.title, job.company, job.location, job.deadline, job.paid,
              job.cover_letter_required, job.source, job.source_url, date.today().isoformat(), job.status)
    cur = conn.execute("INSERT OR IGNORE INTO internships VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
    conn.commit()
    return cur.rowcount == 1


def all_rows(conn):
    return conn.execute("SELECT * FROM internships ORDER BY date_found DESC, company, title").fetchall()
