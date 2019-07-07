from .basic import Presenter
import cv2


class CVPresenter(Presenter):
    def __init__(self, title="debug"):
        self.title = title

    def show(self, image):
        cv2.imshow(self.title, image)
        cv2.waitKey(1)

    def stop(self):
        cv2.destroyAllWindows()

    def start(self):
        pass
