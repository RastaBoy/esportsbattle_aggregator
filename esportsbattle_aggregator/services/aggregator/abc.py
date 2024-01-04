import abc
import typing

class IAggregator(abc.ABC):

    @abc.abstractmethod
    def aggragate(self) -> typing.Any:
        '''
        Во время сбора данных можно обновлять Кэш, например
        '''
        ...
