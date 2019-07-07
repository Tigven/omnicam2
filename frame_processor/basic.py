from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Any, Dict, Optional, Tuple


class FrameProcessor(ABC):
    def __init__(self, bounds: Dict[str, Tuple[Tuple[int, int], Tuple[int, int]]]):
        self.bounds = bounds

    @abstractmethod
    def get_labeled_imgs(self, frame: Any) -> Dict[str, Any]:
        """
        Return cropped images from frame's bounding boxes

        Arguments:
            frame {Any} -- frame

        Returns:
            Dict[str, Any] -- labeled images from bounding boxes
        """
        ...

    @abstractmethod
    def show_bounding_boxes(
        self, frame: Any, status: Optional[Dict[str, bool]] = {}
    ) -> Any:
        """
        Draw bounding bounds on frame

        Arguments:
            frame {Any} -- frame

        Keyword Arguments:
            status {Optional[Dict[str, bool]]} -- status of bounding boxes (default: {{}})

        Returns:
            {Any} -- Frame with bounding boxes
        """

    def get_changed_labeled_imgs(self, frame: Any) -> Dict[str, Any]:
        """
        Return changed images from frame's bounding boxes

        Arguments:
            frame {Any} -- frame to process

        Returns:
            labeled_imgs {Dict[str, Any]} -- only changed images with labels
        """
