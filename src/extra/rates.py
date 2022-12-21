import csv
from xml.etree import ElementTree
from collections import Counter
from datetime import datetime
import requests
from pathlib import Path

from typing import Dict

current_dir = Path(__file__).parent


def get_counts(file_name: str):
    """Возвращает словарь с количеством встречаемости валюты и минимальную и максимальную дату публикации вакансии."""
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        _ = next(reader)
        currencies = []
        published_at = []
        for row in reader:
            if row[3] != "":
                currencies.append(row[3])
            if row[5] != "":
                d = datetime.fromisoformat(row[5].split("+")[0])
                published_at.append(d)
        common = dict(Counter(currencies).most_common())
        print(common)
        print(min(published_at), max(published_at))
        return common, min(published_at), max(published_at)


def get_rates(
    common: Dict[str, int], min_published_at: datetime, max_published_at: datetime
):
    """Создаёт файл с курсами валют за указанный период."""
    date_req1 = min_published_at.strftime("%d/%m/%Y")
    date_req2 = max_published_at.strftime("%d/%m/%Y")
    vals = {
        "USD": "R01235",
        "KZT": "R01335",
        "BYR": "R01090",
        "UAH": "R01720",
        "EUR": "R01239",
    }
    data = [["Date", *vals.keys()]]
    for y in range(min_published_at.year, max_published_at.year + 1):
        for m in range(1, 12 + 1):
            date = datetime.strftime(datetime(y, m, 1), "%Y-%m")
            row = [date] + [""] * len(vals)
            data.append(row)
    currency_data = {currency: {} for currency in vals.keys()}
    for currency, code in vals.items():
        r = requests.get(
            f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_req1}&date_req2={date_req2}&VAL_NM_RQ={code}"
        )
        root = ElementTree.fromstring(r.text)
        for child in root:
            date = datetime.strptime(child.attrib["Date"], "%d.%m.%Y").strftime("%Y-%m")
            current_date_data: list = currency_data[currency].setdefault(date, [])
            for subchild in child:
                if subchild.tag == "Value":
                    value = subchild.text.replace(",", ".")
                if subchild.tag == "Nominal":
                    nominal = subchild.text.replace(",", ".")
            current_date_data.append(float(value) / float(nominal))
    for currency, date_data in currency_data.items():
        for date, values in date_data.items():
            currency_data[currency][date] = sum(values) / len(values)
    for row in data[1:]:
        date = row[0]
        for i, currency in enumerate(vals.keys()):
            row[i + 1] = currency_data[currency].get(date, "")
    with open(current_dir / "rates.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == "__main__":
    data = get_counts(input("Путь до файла: "))
    get_rates(*data)
