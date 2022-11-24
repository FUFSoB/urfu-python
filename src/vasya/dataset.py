import csv

from .vacancy import Vacancy
from .errors import VasyaException

from typing import TYPE_CHECKING, Any, Callable, Generator, Iterator, List

if TYPE_CHECKING:
    from typing_extensions import Self
else:
    Self = Any


class DataSet:
    """Универсальный парсер CSV"""

    def __init__(self, file_name: str, reader: csv.DictReader) -> None:
        self.file_name = file_name
        self._reader = reader
        self._vacancies = (
            Vacancy(**row) for row in reader if all(row) and all(row.values())
        )

    def __iter__(self) -> Iterator[Vacancy]:
        return iter(self._vacancies)

    def __bool__(self) -> bool:
        return bool(self._vacancies)

    def __len__(self) -> int:
        return len(self._vacancies)

    @classmethod
    def from_file(cls, file_name: str) -> "DataSet":
        """Создает экземпляр класса из CSV-файла"""
        file = open(file_name, "r", encoding="utf-8-sig")

        if not file.readline():
            raise VasyaException("Пустой файл")
        if not file.readline():
            raise VasyaException("Нет данных")

        file.seek(0)
        reader = csv.DictReader(file)
        return cls(file_name, reader)

    def apply_filter(self, filter: Callable[[Vacancy], bool]) -> Self:
        """Применяет фильтр к данным"""
        self._vacancies = (i for i in self._vacancies if filter(i))
        return self

    def apply_sort(self, key: Callable[[Vacancy], Any], reverse: bool = False) -> Self:
        """Применяет сортировку к данным"""
        self._vacancies = sorted(self._vacancies, key=key, reverse=reverse)
        return self

    def to_list(self) -> List[Vacancy]:
        """Возвращает данные в виде списка"""
        if isinstance(self._vacancies, Generator):
            self._vacancies = list(self._vacancies)
        return self._vacancies
