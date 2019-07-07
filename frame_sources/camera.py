from threading import Thread

import cv2
import numpy as np

from .basic import FrameSource


class WebcamVideoStream(FrameSource):
    def __init__(
        self, src: int = 0, width: int = 3264, height: int = 2448, fps: int = 25
    ):
        """
        Initialize the video camera stream and read the first frame
        from the stream

        Keyword Arguments:
            src {int} -- index of video device (/dev/video{}) (default: {0})
            width {int} -- width of frame (default: {3264})
            height {int} -- height of frame (default: {2448})
            fps {int} -- framerate of camera (default: {25})
        """
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_FPS, fps)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self) -> 'WebcamVideoStream':
        """
        Start the thread to read frames from the video stream
        """
        Thread(target=self.update, args=()).start()
        return self

    def update(self) -> None:
        """
        Keep looping infinitely until the thread is stopped
        """
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self) -> np.array:
        """
        Return the frame most recently read
        """
        return self.frame

    def stop(self) -> None:
        """
        Indicate that the thread should be stopped
        """
        self.stopped = True
