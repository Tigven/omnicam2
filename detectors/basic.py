from abc import ABC, abstractmethod
from typing import Any, Dict


class Detector(ABC):
    """
    Abstract class for detector
    """

    @abstractmethod
    def detect(self, imgs: Dict[str, Any]) -> Dict[str, bool]:
        """
        Detect objects on image

        Arguments:
            imgs {Dict[str, Any]} -- dictionary with labels and images

        Returns:
            Dict[str, bool] -- dictionary with labels and result of detection
        """
