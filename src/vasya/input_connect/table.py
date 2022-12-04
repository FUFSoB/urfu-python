from .base import InputConnect
from ..dataset import DataSet
from ..vacancy import Vacancy
from ..errors import VasyaException

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)

import prettytable

MISSING = object()


class InputConnectTable(InputConnect):
    """
    Класс-коннектор для генерации таблицы

    Attributes
    ----------
    file_name: str
        Путь до файла
    filter_by: Optional[Tuple[str, str]]
        Кортеж, содержащий ключ и значение для фильтрации
    sort_by: Optional[str]
        Ключ для сортировки
    reverse_sort: bool
        Обратная сортировка
    limit: List[int]
        Список, содержащий границы вывода таблицы
    needed_columns: List[str]
        Список, содержащий названия колонок, которые нужно вывести
    """

    _data: DataSet = None
    _prepared_data: List[Vacancy] = MISSING

    def __init__(
        self,
        file_name: str,
        filter_by: Optional[Tuple[str, str]],
        sort_by: Optional[str],
        reverse_sort: bool,
        limit: List[int],
        needed_columns: List[str],
    ) -> None:
        """
        Конструктор класса.

        Parameters
        ----------
        file_name: str
            Путь до файла
        filter_by: Optional[Tuple[str, str]]
            Кортеж, содержащий ключ и значение для фильтрации
        sort_by: Optional[str]
            Ключ для сортировки
        reverse_sort: bool
            Обратная сортировка
        limit: List[int]
            Список, содержащий границы вывода таблицы
        needed_columns: List[str]
            Список, содержащий названия колонок, которые нужно вывести
        """
        self.file_name = file_name
        self.filter_by = filter_by
        self.sort_by = sort_by
        self.reverse_sort = reverse_sort
        self.limit = limit
        self.needed_columns = needed_columns

    @classmethod
    def from_input(cls) -> "InputConnectTable":
        """
        Метод для создания объекта класса по вводу пользователя.

        Raises
        ------
        VasyaException
            Ввод некорректен

        Returns
        -------
        InputConnectTable
            Экземпляр класса
        """

        file_name = input("Введите название файла: ")
        filter_by = input("Введите параметр фильтрации: ").split(": ")
        sort_by = input("Введите параметр сортировки: ") or None
        reverse_sort = input("Обратный порядок сортировки (Да / Нет): ") or "Нет"
        limit = [int(i) for i in input("Введите диапазон вывода: ").split()]
        needed_headers = [
            i for i in input("Введите требуемые столбцы: ").split(", ") if i
        ]

        if filter_by[0] or len(filter_by) > 1:
            if len(filter_by) != 2:
                raise VasyaException("Формат ввода некорректен")
            if filter_by[0] not in Vacancy.reverse_key_names:
                raise VasyaException("Параметр поиска некорректен")
        elif not filter_by[0]:
            filter_by = None

        if sort_by and sort_by not in Vacancy.reverse_key_names:
            raise VasyaException("Параметр сортировки некорректен")

        if reverse_sort not in ("Да", "Нет"):
            raise VasyaException("Порядок сортировки задан некорректно")
        reverse_sort = reverse_sort == "Да"

        return cls(file_name, filter_by, sort_by, reverse_sort, limit, needed_headers)

    def prepare_data(self) -> None:
        """
        Метод для подготовки данных к выводу.

        Raises
        ------
        VasyaException
            Файл не найден или в нём нет данных
        """
        self._prepared_data = self.get_processed_data().to_list()

    def get_data(self) -> DataSet:
        """
        Возвращает экземпляр класса DataSet

        Raises
        ------
        VasyaException
            Файл не найден или в нём нет данных

        Returns
        -------
        DataSet
            Экземпляр класса DataSet
        """

        return DataSet.from_file(self.file_name)

    def get_processed_data(self) -> DataSet:
        """
        Возвращает экземпляр класса DataSet с применёнными фильтрами и сортировкой

        Raises
        ------
        VasyaException
            Файл не найден или в нём нет данных

        Returns
        -------
        DataSet
            Экземпляр класса DataSet
        """

        data = self.get_data()
        self.apply_filter(data)
        self.apply_sort(data)

        return data

    def apply_filter(self, data: DataSet) -> None:
        """
        Применяет фильтр к экземпляру класса DataSet

        Parameters
        ----------
        data: DataSet
            Экземпляр класса DataSet
        """

        filter_by = self.filter_by
        if filter_by:
            key = Vacancy.reverse_key_names[filter_by[0]]

            filters: Dict[str, Callable[[Vacancy], bool]] = {
                "salary": lambda vacancy: float(filter_by[1]) in vacancy.salary,
                "salary_currency": lambda vacancy: (
                    filter_by[1] == vacancy.salary.salary_currency
                ),
                "published_at": lambda vacancy: (
                    filter_by[1] == vacancy.published_at.strftime("%d.%m.%Y")
                ),
                "key_skills": lambda vacancy: all(
                    skill in vacancy.key_skills for skill in filter_by[1].split(", ")
                ),
            }

            func = filters.get(
                key, lambda vacancy: filter_by[1] == getattr(vacancy, key)
            )
            data.apply_filter(func)

    def apply_sort(self, data: DataSet) -> None:
        """
        Применяет сортировку к экземпляру класса DataSet

        Parameters
        ----------
        data: DataSet
            Экземпляр класса DataSet
        """

        sort_by = self.sort_by
        reverse_sort = self.reverse_sort
        if sort_by:
            key = Vacancy.reverse_key_names[sort_by]
            data.apply_sort(lambda vacancy: getattr(vacancy, key), reverse_sort)

    def get_answer(self, *args, **kwargs) -> None:
        """
        Выводит таблицу в консоль

        Raises
        ------
        VasyaException
            Файл не найден, в нём нет данных или применённые фильтры
            не вернули результатов
        """

        if self._prepared_data is MISSING:
            self.prepare_data()

        data = self._prepared_data
        if not data:
            raise VasyaException("Ничего не найдено")

        limit = self.limit
        needed_headers = self.needed_columns

        table = prettytable.PrettyTable(
            field_names=("№", *Vacancy.ordered_key_names.values()),
            max_width=20,
            align="l",
            hrules=prettytable.ALL,
        )

        for number, vacancy in enumerate(data, start=1):
            row = (number, *vacancy.formatted_data())
            table.add_row(row)

        kwargs: Dict[str, Any] = {}

        if needed_headers:
            kwargs["fields"] = ("№", *needed_headers)

        if limit:
            kwargs["start"] = limit[0] - 1
            if len(limit) > 1:
                kwargs["end"] = limit[1] - 1

        to_print = table.get_string(**kwargs)
        print(to_print)
