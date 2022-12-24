import csv
from datetime import datetime
from pathlib import Path

current_dir = Path(__file__).parent


def number(s: str) -> float:
    """Преобразует строку в число, иначе возвращает 0."""
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return 0


def merge_salary(file_name: str):
    """Объединяет колонки зарплаты и валюты в одну колонку с зарплатой в рублях."""
    rates_data = csv.DictReader(open(current_dir / "rates.csv"))
    rates = {}
    for row in rates_data:
        rates[row["Date"]] = row
    result = [["name", "salary", "area_name", "published_at"]]

    with open(file_name, "r") as f:
        reader = csv.reader(f)
        _ = next(reader)
        for row in reader:
            n1 = number(row[1])
            n2 = number(row[2])
            s = (n1 + n2) / ((bool(n1) + bool(n2)) or 1)
            if s != 0 and row[3] != "":
                date = datetime.fromisoformat(row[5].split("+")[0]).strftime("%Y-%m")
                if row[3] == "RUR":
                    pass
                elif row[3] not in rates[date]:
                    continue
                else:
                    rate = number(rates[date][row[3]])
                    s = s * rate
            result.append([row[0], s, row[4], row[5]])
    with open(current_dir / "salary.csv", "w") as f:
        result_writer = csv.writer(f)
        result_writer.writerows(result)


if __name__ == "__main__":
    merge_salary(input("Путь к файлу: "))
