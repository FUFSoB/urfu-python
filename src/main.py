#!./venv/bin/python

from vasya import InputConnectReport, InputConnectTable, VasyaException
from pathlib import Path

from typing import Dict
from vasya import InputConnectBase

current_dir = Path(__file__).parent


def main():
    choices: Dict[str, InputConnectBase] = {
        "вакансии": InputConnectTable,
        "статистика": InputConnectReport,
    }
    while True:
        choice = input("Введите действие (вакансии / статистика): ").lower()
        if not choices.get(choice):
            print("Неверный ввод")
            continue
        try:
            input_connect = choices[choice].from_input()
            input_connect.prepare_data()
            input_connect.get_answer(
                template_path=str(current_dir / "pdf_template.html")
            )
        except VasyaException as ex:
            print(ex)
        break


if __name__ == "__main__":
    main()
