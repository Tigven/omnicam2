from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from config.file import FileConfig
from detectors.random_detector import DebugDetector, RandomDetector
from frame_processor.cv import CVFrameProcessor
from frame_sources.camera import WebcamVideoStream
from presenter.flask import FlaskPresenter
from sender.http_sender import HTTPSender

if __name__ == "__main__":

    config = FileConfig("config.yaml")
    source = WebcamVideoStream(0, 640, 480, 1)
    processor = CVFrameProcessor(config.bounds)
    detector = RandomDetector()
    sender = HTTPSender(config.cam_id, config.backend)
    presenter = FlaskPresenter()

    pool = ProcessPoolExecutor()

    detect_in_progress: bool = False
    prev_status: dict = {}
    status: dict = {}

    try:
        source.start()
        presenter.start()
        while True:
            frame = source.read()
            imgs = processor.get_changed_labeled_imgs(frame)
            if imgs and not detect_in_progress:
                future = pool.submit(detector.detect, imgs)
                detect_in_progress = True
            if future and future.done():
                detect_in_progress = False
                status = future.result()
                future = None
            if status != prev_status:
                sender.send(status)
                prev_status = status
            frame = processor.show_bounding_boxes(frame, status)
            frame = processor.show_labels(frame)
            presenter.show(frame)
    finally:
        source.stop()
        presenter.stop()
