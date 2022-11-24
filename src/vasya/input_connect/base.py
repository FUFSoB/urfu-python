from abc import ABCMeta, abstractmethod, abstractclassmethod


class InputConnect(metaclass=ABCMeta):
    """
    Абстрактный класс для класса-коннектора между входными данными,
    их обработкой и выходными данными.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Инициализация коннектора.
        Наследники могут принимать любые аргументы,
        а также инициализировать любые атрибуты.
        """
        ...

    @abstractclassmethod
    def from_input(cls) -> "InputConnect":
        """
        Метод для создания экземпляра класса-коннектора из входных данных.
        """
        ...

    @abstractmethod
    def prepare_data(self, *args, **kwargs) -> None:
        """
        Метод для обработки данных для последующей выдачи.
        Наследники могут принимать любые аргументы,
        """
        ...

    @abstractmethod
    def get_answer(self, *args, **kwargs) -> None:
        """
        Метод для получения результата обработки входных данных.
        Наследники могут принимать любые аргументы,
        """
        ...
