import yaml


class FileConfig:
    def __init__(self, filename):
        with open(filename) as f:
            config = yaml.load(f)
        self.backend = config.get("backend_server")
        self.cam_id = config.get("cam_id")
        self.camera_num = config.get("camera_num", 1)
        self.collect_dataset = config.get("collect_dataset", 0)
        self.show_spots = config.get("show_spots", True)
        self.bounds = config.get("bounds", {})
