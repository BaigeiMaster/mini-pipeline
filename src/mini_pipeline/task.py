from abc import ABC, abstractmethod
from typing import Any, Union


class BaseTask(ABC):

    def __init__(self, receiver_id: Union[int, None] = None):
        assert isinstance(
            receiver_id, Union[int, None, tuple, list]
        ), f"{self}: receiver_id 必须为 int, tuple[int], list[int] 类型"
        self._id = None
        self._receiver_id = receiver_id

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self._id}, receiver_id={self._receiver_id})"
        )

    @abstractmethod
    def run(self, arg) -> dict[int, Any]:
        pass

    @property
    def receiver_id(self):
        return self._receiver_id

    @receiver_id.setter
    def receiver_id(self, receiver_id: int):
        self._receiver_id = receiver_id

    @property
    def id_(self) -> int:
        return self._id

    @id_.setter
    def id_(self, id_: int):
        self._id = id_
