import csv
from pathlib import Path

current_dir = Path(__file__).parent


def split_csv_by_year(csv_file_path: str) -> None:
    """
    Функция для разделения csv на отдельные файлы по годам
    Файлы сохраняются в той же директории, где находится скрипт

    Parameters
    ----------
    csv_file_path: str
        Путь до файла
    """

    csv_path = Path(csv_file_path)
    csv_file_name = csv_path.name

    with open(csv_path, "r", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        header = next(reader)
        date_index = header.index("published_at")
        data = [row for row in reader if all(row)]

    years = set(row[date_index].split("-")[0] for row in data)

    for year in years:
        with open(
            current_dir / f"{csv_file_name.rsplit('.', 1)[0]}_{year}.csv",
            "w",
            encoding="utf-8-sig",
        ) as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(header)
            writer.writerows(
                row for row in data if row[date_index].split("-")[0] == year
            )


if __name__ == "__main__":
    split_csv_by_year(input("Введите путь до файла: "))
