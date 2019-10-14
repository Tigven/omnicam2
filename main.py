from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import time
from config.file import FileConfig
from detectors.fast_ai import FastAIDetector
from frame_processor.cv import CVFrameProcessor
from frame_sources.camera import WebcamVideoStream
from presenter.flask import FlaskPresenter
from sender.http_sender import HTTPSender

if __name__ == "__main__":

    config = FileConfig("config.yaml")
    sources = []
    processors = []
    presenters = []
    detect_states = []
    prev_statuses = []
    statuses = []
    futures = []


    for camera_num in range(config.camera_num):
        sources.append(WebcamVideoStream(camera_num))
        processors.append(CVFrameProcessor(config.bounds[camera_num]))
        detect_states.append(False)
        prev_statuses.append({})
        statuses.append({})
        futures.append(None)

    detector = FastAIDetector(
        'resnet18', 64, '/home/odroid/omnicam/dummy/', '64_urban')
    sender = HTTPSender(config.cam_id, config.backend)
    presenter = FlaskPresenter()

    pool = ThreadPoolExecutor()
    port = 5000
    try:
        for source in sources:
            source.start()
            time.sleep(1)
            presenters.append(FlaskPresenter(port).start())
            port += 1

        while True:
            for i, (source, processor) in enumerate(zip(sources, processors)):
                frame = source.read()
                imgs = processor.get_changed_labeled_imgs(frame)
                if imgs and not detect_states[i]:
                    statuses[i] = detector.detect(imgs)
                    futures[i] = pool.submit(detector.detect, imgs)
                    detect_states[i] = True
                if futures[i] and futures[i].done():
                    detect_states[i] = False
                    statuses[i] = futures[i].result()
                    futures[i] = None
                sender.send(statuses[i])
                if statuses[i] != prev_statuses[i]:
                    # sender.send(statuses[i])
                    prev_statuses[i] = statuses[i]
                frame = processor.show_bounding_boxes(frame, statuses[i])
                frame = processor.show_labels(frame)
                presenters[i].show(frame)
    finally:
        for source in sources:
            source.stop()

        for presenter in presenters:
            presenter.stop()
