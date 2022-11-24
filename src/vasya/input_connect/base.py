from abc import ABCMeta, abstractmethod, abstractclassmethod


class InputConnect(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs) -> None:
        ...

    @abstractclassmethod
    def from_input(cls) -> "InputConnect":
        ...

    @abstractmethod
    def prepare_data(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def get_answer(self, *args, **kwargs) -> None:
        ...
