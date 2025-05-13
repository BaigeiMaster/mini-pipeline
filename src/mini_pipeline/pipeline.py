from abc import ABC, abstractmethod
from typing import Any, Union

from .task import BaseTask


class Pipeline(BaseTask):

    def __init__(
        self,
        tasks: Union[list[BaseTask], None] = None,
        chained: bool = True,
        receiver_id: Union[int, None] = None,
    ):
        super().__init__(receiver_id=receiver_id)

        self._results = {}
        self._chained = chained
        self._tasks = tasks if tasks is not None else []
        assert all(
            isinstance(task, BaseTask) for task in self._tasks
        ), f"{self}: tasks must be a list of BaseTask instances"
        self._inited = False

    def __repr__(self):
        return f"{self.__class__.__name__}(tasks={self._tasks}, chained={self._chained}, id={self.id_}, receiver_id={self.receiver_id})"

    def init(self):
        assert isinstance(self.tasks, list), f"{self}: tasks must be list"
        assert all(
            isinstance(task, BaseTask) for task in self.tasks
        ), f"{self}: tasks must be a list of BaseTask instances"
        for i, t in enumerate(self.tasks):
            t.id_ = i
        for i, t in enumerate(reversed(self.tasks)):
            t.id_inverse = -(i + 1)
        for t in self.tasks:
            if isinstance(t, Pipeline):
                t.init()
        if self.chained:
            self.create_chain(self.tasks)
        self._inited = True

    def run(self, arg=None) -> Any:
        if not self.inited:
            self.init()
        if arg is not None:
            self.results = {0: arg}

        for i, task in enumerate(self.tasks):

            if self.results is not None and task.id_ in self.results.keys():
                result = task.run(self.results[task.id_])
                del self.results[task.id_]
            else:
                result = task.run()
            receiver_id = task.receiver_id

            if receiver_id is not None and result is not None:
                # 多个receiver的情况
                if isinstance(receiver_id, Union[list, tuple]):
                    for r in receiver_id:
                        new_r = r if r >= 0 else len(self.tasks) + r
                        if new_r <= task.id_:
                            print(
                                f"Warning: {task} receiver_id less or equal to task id {task.id_}, return will be ignored"
                            )
                            continue
                        self.results = {new_r: result}
                else:
                    new_r = (
                        receiver_id
                        if receiver_id >= 0
                        else len(self.tasks) + receiver_id
                    )
                    if new_r <= task.id_:
                        print(
                            f"Warning: {task} receiver_id less or equal to task id {task.id_}, return will be ignored"
                        )
                        continue
                    self.results = {new_r: result}

            # 最后一个返回值
            if i == len(self.tasks) - 1:
                return result

    def __add__(self, task: Union[BaseTask, list[BaseTask]]):
        assert not self.inited, f"{self}: pipeline has been inited, can't add task"
        if isinstance(task, list):
            assert all(
                isinstance(t, BaseTask) for t in task
            ), f"{self}: tasks must be a list[list] of BaseTask instances"
        else:
            assert isinstance(
                task, BaseTask
            ), f"{self}: tasks must be a list of BaseTask instances"

        new_tasks = self.tasks.copy()
        if isinstance(task, list):
            new_tasks.extend(task)
        else:
            new_tasks.append(task)
        return Pipeline(
            tasks=new_tasks,
            chained=self.chained,
            receiver_id=self.receiver_id,
        )

    def add(self, task: BaseTask) -> None:
        assert not self.inited, f"{self}: pipeline has been inited, can't add task"
        if isinstance(task, list):
            assert all(
                isinstance(t, BaseTask) for t in task
            ), f"{self}: tasks must be a list[list] of BaseTask instances"
        else:
            assert isinstance(
                task, BaseTask
            ), f"{self}: tasks must be a list of BaseTask instances"

        if isinstance(task, list):
            self.tasks.extend(task)
        else:
            self.tasks.append(task)

    def create_chain(self, tasks: list[BaseTask]) -> None:
        for i, task in enumerate(tasks):
            if task.receiver_id is None:
                task.receiver_id = i + 1
        tasks[-1].receiver_id = None

    @property
    def inited(self):
        return self._inited

    @property
    def tasks(self) -> list[BaseTask]:
        return self._tasks

    @property
    def chained(self) -> bool:
        return self._chained

    @property
    def results(self) -> dict:
        return self._results

    @results.setter
    def results(self, results: dict):
        assert isinstance(results, dict), f"{self}: results must be dict"
        assert all(
            isinstance(key, int) for key in results.keys()
        ), f"{self}: results keys must be int"

        for k in results.keys():
            # 多数据
            if (
                k in self._results.keys()
                and not isinstance(self._results[k], list)
                and not isinstance(results[k], dict)
            ):
                self._results[k] = [self._results[k]]
                self._results[k].append(results[k])
            # 返回为dict
            elif (
                k in self._results.keys()
                and not isinstance(self._results[k], list)
                and isinstance(results[k], dict)
            ):
                self._results[k].update(results[k])
            elif k in self._results.keys() and isinstance(self._results[k], list):
                self._results[k].append(results[k])
            # 单数据
            else:
                self._results[k] = results[k]
