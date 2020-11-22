from abc import ABC, ABCMeta, abstractmethod
from ..models import OutgoingEmail
from ..exceptions import TaskException


class Task(ABC):
    __metaclass__ = ABCMeta

    def do(self, *args) -> OutgoingEmail:
        try:
            return self.do_task(*args)
        except Exception as e:
            raise TaskException(e)

    @abstractmethod
    def do_task(self, *args) -> OutgoingEmail:
        pass


