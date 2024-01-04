import abc
import typing

from ..api.abc import ApiService

class IAggregator(abc.ABC):

    @abc.abstractmethod
    def aggragate(self) -> typing.Any:
        ...
