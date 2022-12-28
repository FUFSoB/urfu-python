import csv
import sqlite3
from pathlib import Path

current_dir = Path(__file__).parent
db_path = current_dir / "rates.sqlite"
csv_path = current_dir / "rates.csv"


def csv_to_sql():
    with open(csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        _ = next(reader)
        with sqlite3.connect(db_path) as conn:
            conn.execute("DROP TABLE IF EXISTS rates")
            conn.execute(
                """
                CREATE TABLE rates (
                    date TEXT,
                    BYR REAL,
                    USD REAL,
                    EUR REAL,
                    KZT REAL,
                    UAH REAL,
                    AZN REAL,
                    KGS REAL,
                    UZS REAL,
                    PRIMARY KEY(date)
                )"""
            )
            while True:
                data = next(reader, None)
                if data is None:
                    break
                data = (
                    data[0],
                    *map(lambda x: x and float(x) or None, data[1:]),
                    None,
                    None,
                    None,
                )
                print(data)
                conn.execute(
                    "INSERT INTO rates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data
                )
            conn.commit()


if __name__ == "__main__":
    csv_to_sql()
