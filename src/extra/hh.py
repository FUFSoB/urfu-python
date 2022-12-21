import csv
import requests
from pathlib import Path
from datetime import datetime, timedelta

current_dir = Path(__file__).parent


def get_hh_data(date: datetime, period: timedelta = timedelta(minutes=120)):
    """Собирает данные с hh.ru за указанный период."""
    final_data = [
        [
            "name",
            "salary_from",
            "salary_to",
            "salary_currency",
            "area_name",
            "published_at",
        ]
    ]
    date = date.replace(microsecond=0)
    orient_date = date + timedelta(days=1)
    date -= period
    while True:
        date += period
        if date <= orient_date:
            break
        page = 0
        while True:
            page += 1
            url = f"https://api.hh.ru/vacancies?date_from={date.isoformat()}&date_to={(date + period).isoformat()}&per_page=100&page={page}&specialization=1"
            response = requests.get(url)
            print(response, repr(response.text))
            if response.status_code != 200:
                break
            data = response.json()
            for item in data["items"]:
                if item["salary"] is None:
                    continue
                final_data.append(
                    [
                        item["name"],
                        item["salary"]["from"],
                        item["salary"]["to"],
                        item["salary"]["currency"],
                        item["area"]["name"],
                        item["published_at"],
                    ]
                )
            if page + 1 >= data["pages"]:
                break
    with open(current_dir / "hh.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(final_data)


if __name__ == "__main__":
    get_hh_data(datetime(2022, 12, 21))
