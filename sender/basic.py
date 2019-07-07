from abc import ABC, abstractmethod
from typing import Dict


class Sender(ABC):
    """
    Class to send results
    """

    @abstractmethod
    def send(self, status: Dict[str, bool]) -> None:
        """
        Send results

        Arguments:
            status {Dict[str, bool]} -- status from detector
        """


class DebugSender(Sender):
    def send(self, status):
        print(status)
