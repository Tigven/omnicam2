from abc import ABC, abstractmethod
from typing import Any


class FrameSource(ABC):
    """Abstract class for frame sources (e.g. webcamera)
    """

    @abstractmethod
    def read(self) -> Any:
        """Get image from source

        Returns:
            Any -- image
        """
