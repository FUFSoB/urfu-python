from datetime import datetime
import re

from typing import TYPE_CHECKING, Any, Generator, Optional, Union

if TYPE_CHECKING:
    from typing_extensions import Self
else:
    Self = Any


class skillslist(list):
    """
    Список для упрощения работы с навыками
    """

    def __lt__(self, other: list) -> bool:
        if not isinstance(other, list):
            return NotImplemented
        return len(self) < len(other)

    def __str__(self) -> str:
        return "\n".join(self)


class Currency:
    """
    Класс валюты с курсом к рублю

    Attributes
    ----------
    code: str
        Код валюты
    name: str
        Название валюты
    rate_to_rub: float
        Курс к рублю
    """

    def __init__(self, code: str, name: str, rate_to_rub: float) -> None:
        """
        Инициализация класса

        Parameters
        ----------
        code: str
            Код валюты
        name: str
            Название валюты
        rate_to_rub: float
            Курс к рублю
        """

        self.code = code
        self.name = name
        self.rate_to_rub = float(rate_to_rub)

    def __str__(self) -> str:
        return self.code

    def __eq__(self, other: str) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        return self.code == other or self.name == other

    def convert_to_rub(self, value: float) -> float:
        """
        Конвертирует валюту в рубли

        Parameters
        ----------
        value: float
            Сумма в валюте

        Returns
        -------
        float
            Сумма в рублях
        """

        return value * self.rate_to_rub

    __mul__ = convert_to_rub
    __rmul__ = convert_to_rub


currency_dict = {
    i.code: i
    for i in (
        Currency("AZN", "Манаты", 35.68),
        Currency("BYR", "Белорусские рубли", 23.91),
        Currency("EUR", "Евро", 59.90),
        Currency("GEL", "Грузинский лари", 21.74),
        Currency("KGS", "Киргизский сом", 0.76),
        Currency("KZT", "Тенге", 0.13),
        Currency("RUR", "Рубли", 1),
        Currency("UAH", "Гривны", 1.64),
        Currency("USD", "Доллары", 60.66),
        Currency("UZS", "Узбекский сум", 0.0055),
    )
}


class Salary:
    """
    Устанавливает все основные поля зарплаты, а также метод
    для перевода зарплаты в рубли в случае необходимости

    Attributes
    ----------
    salary_from: float
        Нижняя граница зарплаты
    salary_to: float
        Верхняя граница зарплаты
    salary_gross: bool
        Зарплата указана до вычета налогов
    salary_currency: Currency
        Валюта зарплаты
    """

    def __init__(
        self,
        salary_from: float,
        salary_to: float,
        salary_gross: bool,
        salary_currency: Currency,
    ) -> None:
        """
        Инициализация класса

        Parameters
        ----------
        salary_from: float
            Нижняя граница зарплаты
        salary_to: float
            Верхняя граница зарплаты
        salary_gross: bool
            Зарплата указана до вычета налогов
        salary_currency: Currency
            Валюта зарплаты
        """

        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def __repr__(self) -> str:
        return f"{self.salary_from}-{self.salary_to} {self.salary_currency} ({self.salary_gross})"

    def __eq__(self, other: "Salary") -> bool:
        if not isinstance(other, Salary):
            return NotImplemented
        return (
            self.salary_from == other.salary_from
            and self.salary_to == other.salary_to
            and self.salary_gross == other.salary_gross
            and self.salary_currency == other.salary_currency
        )

    def __float__(self) -> float:
        return (self.salary_from + self.salary_to) / 2

    def __lt__(self, other: "Salary") -> bool:
        if not isinstance(other, Salary):
            return NotImplemented

        rub = self.to_rub()
        other_rub = other.to_rub()
        return float(rub) < float(other_rub)

    def __contains__(self, item: float) -> bool:
        return self.salary_from <= item <= self.salary_to

    def __str__(self) -> str:
        salary_from = int(self.salary_from)
        salary_to = int(self.salary_to)
        salary_currency = self.salary_currency.name
        salary_gross = self.salary_gross and "Без вычета налогов" or "С вычетом налогов"
        return f"{salary_from:,} - {salary_to:,} ({salary_currency}) ({salary_gross})".replace(
            ",", " "
        )

    def to_rub(self) -> "Salary":
        """
        Переводит зарплату в рубли

        Returns
        -------
        Salary
            Новый объект с зарплатой в рублях
        """

        if self.salary_currency == "RUR":
            return self
        return Salary(
            self.salary_currency * self.salary_from,
            self.salary_currency * self.salary_to,
            self.salary_gross,
            currency_dict["RUR"],
        )


Element = Union[str, Salary, skillslist, datetime]


class Experience(str):
    """
    Класс для упрощения работы со строками опыта работы

    Attributes
    ----------
    order: int
        Порядковый номер опыта работы
    """

    order: int = -1

    def set_order(self, order: int) -> Self:
        """
        Устанавливает порядковый номер опыта работы

        Parameters
        ----------
        order: int
            Порядковый номер опыта работы
        """

        self.order = order
        return self

    def __lt__(self, other: "Experience") -> bool:
        if not isinstance(other, Experience):
            return NotImplemented
        return self.order < other.order


experience_dict = {
    "noExperience": Experience("Нет опыта").set_order(0),
    "between1And3": Experience("От 1 года до 3 лет").set_order(1),
    "between3And6": Experience("От 3 до 6 лет").set_order(2),
    "moreThan6": Experience("Более 6 лет").set_order(3),
}


class Vacancy:
    """
    Устанавливает все основные поля вакансии

    Attributes
    ----------
    name: str
        Название вакансии
    salary_rub: float
        Зарплата в рублях
    area_name: str
        Название города
    published_at: datetime
        Дата публикации вакансии
    description: Optional[str]
        Описание вакансии
    key_skills: Optional[skillslist]
        Список ключевых навыков
    experience: Optional[Experience]
        Опыт работы
    premium: Optional[str]
        Премиум вакансия (Да/Нет)
    employer_name: Optional[str]
        Название компании
    salary: Optional[Salary]
        Зарплата
    """

    ordered_key_names = {
        "name": "Название",
        "description": "Описание",
        "key_skills": "Навыки",
        "experience": "Опыт работы",
        "premium": "Премиум-вакансия",
        "employer_name": "Компания",
        "salary": "Оклад",
        "area_name": "Название региона",
        "published_at": "Дата публикации вакансии",
    }

    key_names = {
        **ordered_key_names,
        # other
        "salary_from": "Нижняя граница вилки оклада",
        "salary_to": "Верхняя граница вилки оклада",
        "salary_gross": "Оклад указан до вычета налогов",
        "salary_currency": "Идентификатор валюты оклада",
    }

    reverse_key_names = {v: k for k, v in key_names.items()}

    re_tags = re.compile(r"<.+?>")

    @classmethod
    def _str(cls, value: str) -> str:
        """
        Удаляет теги из строки

        Parameters
        ----------
        value: str
            Строка

        Returns
        -------
        str
            Строка без тегов
        """

        return "\r\n".join(
            " ".join(i.split()) for i in cls.re_tags.sub("", value).split("\r\n")
        ).strip()

    # @staticmethod
    # def _parse_time(value: str) -> datetime:  # test1
    #     return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S%z")

    @staticmethod
    def _parse_time(value: str) -> datetime:  # test2
        return datetime.fromisoformat(value.split("+")[0])

    # @staticmethod
    # def _parse_time(value: str) -> datetime:  # test3
    #     split = value.split("+")[0].split("T")
    #     return datetime(*map(int, split[0].split("-") + split[1].split(":")))

    # @staticmethod
    # def _parse_time(value: str) -> datetime:  # test4
    #     split = value.split("+")[0].split("T")
    #     return datetime(
    #         int(split[0].split("-")[0]),
    #         int(split[0].split("-")[1]),
    #         int(split[0].split("-")[2]),
    #         int(split[1].split(":")[0]),
    #         int(split[1].split(":")[1]),
    #         int(split[1].split(":")[2]),
    #     )

    def __init__(
        self,
        *,
        name: str,
        salary_from: str,
        salary_to: str,
        salary_currency: str,
        area_name: str,
        published_at: str,
        # full
        description: Optional[str] = None,
        key_skills: Optional[str] = None,
        experience_id: Optional[str] = None,
        premium: Optional[str] = None,
        employer_name: Optional[str] = None,
        salary_gross: Optional[str] = None,
    ) -> None:
        """
        Инициализация класса

        Parameters
        ----------
        name: str
            Название вакансии
        salary_from: str
            Нижняя граница оклада
        salary_to: str
            Верхняя граница оклада
        salary_currency: str
            Идентификатор валюты оклада
        area_name: str
            Название города
        published_at: str
            Дата публикации вакансии
        description: Optional[str]
            Описание вакансии
        key_skills: Optional[str]
            Список ключевых навыков
        experience_id: Optional[str]
            Идентификатор опыта работы
        premium: Optional[str]
            Премиум вакансия (true/false)
        employer_name: Optional[str]
            Название компании
        salary_gross: Optional[str]
            Оклад указан до вычета налогов (true/false)
        """

        self.name = self._str(name)

        self.salary_rub = (
            (float(salary_from) + float(salary_to)) / 2 * currency_dict[salary_currency]
        )

        self.area_name = area_name
        self.published_at = self._parse_time(published_at)

        self.description = self._str(description) if description else None
        self.key_skills = skillslist(key_skills.split("\n")) if key_skills else None
        self.experience = experience_dict[experience_id] if experience_id else None

        self.premium = (
            ("Да" if premium.lower() == "true" else "Нет") if premium else None
        )
        self.employer_name = self._str(employer_name) if employer_name else None

        self.salary = (
            Salary(
                float(salary_from),
                float(salary_to),
                salary_gross.lower() == "true",
                currency_dict[salary_currency],
            )
            if salary_gross
            else None
        )

    def formatted_data(self) -> Generator[Element, None, None]:
        """
        Возвращает данные вакансии, подготовленные для вывода

        Returns
        -------
        Generator[Element, None, None]
            Данные вакансии
        """

        MISSING = object()
        for key in self.ordered_key_names:
            data: Element = getattr(self, key, MISSING)
            if data is MISSING:
                continue

            if key == "published_at":
                data = data.strftime("%d.%m.%Y")

            data = str(data)
            if len(data) > 100:
                data = data[:100] + "..."

            yield data
