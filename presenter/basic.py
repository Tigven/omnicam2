from abc import ABC, abstractmethod
from typing import Any


class Presenter(ABC):
    """
    Basic class for image presenter
    """

    @abstractmethod
    def start(self):
        """
        Start presenter
        """

    @abstractmethod
    def show(self, frame: Any) -> None:
        """
        Show image

        Arguments:
            frame {[type]} -- image to show
        """

    @abstractmethod
    def stop(self) -> None:
        """
        Destructor for presenter
        """
