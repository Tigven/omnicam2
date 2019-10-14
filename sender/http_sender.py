from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import requests

from .basic import Sender


class HTTPSender(Sender):
    def __init__(self, cam_id, backend):
        self.backend = backend
        self.cam_id = cam_id
        self.pool = ProcessPoolExecutor()

    def prepare_data(self, status):
        payload = {
            label: "occupied" if occupied else "empty"
            for (label, occupied) in status.items()
        }
        post_data = {
            "vendor_type": "OMNI",
            "uri": self.cam_id,
            "payload": payload
            }
        return post_data

    def _send(self, post_data, timeout=3):
        try:
            r = requests.post(
                "{}/api/v1/omnipark/parking_data/".format(self.backend),
                json=post_data,
                timeout=timeout,
            )
            print("Send {} to {}".format(post_data, self.backend))
        except Exception as e:
            print("Can't connect to {}. Error:".format(self.backend), e)

    def send(self, status):
        if not self.backend:
            print("No backend to send")
            return
        post_data = self.prepare_data(status)
        print("try to send {}".format(post_data))
        self._send(post_data)
        # self.pool.submit(self._send, post_data)

