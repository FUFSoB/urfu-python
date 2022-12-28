import csv
import sqlite3
from pathlib import Path

current_dir = Path(__file__).parent
db_path = current_dir / "salary.sqlite"
csv_path = current_dir / "salary.csv"


def csv_to_sql():
    with open(csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        _ = next(reader)
        with sqlite3.connect(db_path) as conn:
            conn.execute("DROP TABLE IF EXISTS salary")
            conn.execute(
                """
                CREATE TABLE salary (
                    name TEXT,
                    salary REAL,
                    area_name TEXT,
                    published_at TEXT
                )"""
            )
            while True:
                data = next(reader, None)
                if data is None:
                    break
                data[1] = data[1] and float(data[1]) or None
                data[3] = data[3][:7]
                conn.execute("INSERT INTO salary VALUES (?, ?, ?, ?)", data)
            conn.commit()


if __name__ == "__main__":
    csv_to_sql()
