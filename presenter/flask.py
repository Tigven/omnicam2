from threading import Thread

import cv2
from flask import Flask, Response, render_template

from .basic import Presenter


class FlaskPresenter(Presenter):
    def __init__(self, port=5000):
        self.frame = None
        self.port = port

    def show(self, image):
        self.frame = image

    def stop(self):
        pass

    def start(self):
        app = Flask(__name__)

        def gen():
            while True:
                if self.frame is not None:
                    _, jpeg = cv2.imencode(".jpg", self.frame)
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
                    )

        @app.route("/video")
        def video_feed():
            return Response(
                gen(), mimetype="multipart/x-mixed-replace; boundary=frame"
            )

        Thread(target=app.run, args=(["0.0.0.0", self.port])).start()
