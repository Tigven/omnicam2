from .basic import Detector
import random
import time


class RandomDetector(Detector):
    def detect(self, imgs_dict):
        time.sleep(3)
        return {label: random.randint(0, 1) for label in imgs_dict}


class DebugDetector(Detector):
    def __init__(self):
        self.state = True

    def detect(self, imgs_dict):
        time.sleep(3)
        self.state = not self.state
        return {label: self.state for label in imgs_dict}
