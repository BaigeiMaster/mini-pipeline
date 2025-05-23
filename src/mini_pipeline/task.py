from abc import ABC, abstractmethod
from typing import Any, Union, Optional, List, Tuple


class BaseTask(ABC):

    def __init__(self, receiver_id: Optional[Union[int, List, Tuple]] = None):
        assert isinstance(
            receiver_id, Union[int, None, Tuple, List]
        ), f"{self}: receiver_id 必须为 int, tuple[int], list[int] 类型"
        self._id = 0
        self._receiver_id = receiver_id

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self._id}, receiver_id={self._receiver_id})"
        )

    @abstractmethod
    def run(self, arg=None):
        pass

    @property
    def receiver_id(self) -> Union[int, List, Tuple, None]:
        return self._receiver_id

    @receiver_id.setter
    def receiver_id(self, receiver_id: Optional[Union[int, List[int], Tuple[int]]]):
        self._receiver_id = receiver_id

    @property
    def id_(self) -> int:
        return self._id

    @id_.setter
    def id_(self, id_: int):
        self._id = id_
