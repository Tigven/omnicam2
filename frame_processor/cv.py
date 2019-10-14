import cv2
import numpy as np

from .basic import FrameProcessor


class CVFrameProcessor(FrameProcessor):
    def __init__(self, bounds):
        self.bounds = bounds
        self._hists = dict()
        self._rects = dict()
        for label, bound in bounds.items():
            first, second = bound
            self._rects[label] = np.array(
                (first, (first[0], second[1]), second, (second[0], first[1]))
            )

    def show_bounding_boxes(
        self, frame, status, positive_color=(0, 0, 255), negative_color=(0, 255, 0)
    ):
        if frame is None:
            return frame
        for label, state in status.items():
            color = positive_color if state else negative_color
            cv2.drawContours(
                frame,
                [self._rects[label]],
                -1,
                color=color,
                thickness=2,
                lineType=cv2.LINE_8,
            )

        return frame

    def show_labels(self, frame):
        if frame is None:
            return frame
        for label, rects in self._rects.items():
            moments = cv2.moments(rects)
            centroid = (
                int(moments["m10"] / moments["m00"]) - 3,
                int(moments["m01"] / moments["m00"]) + 3,
            )
            for shift_1, shift_2 in [[1, 1], [-1, -1], [1, -1], [-1, 1]]:
                cv2.putText(
                    frame,
                    str(label),
                    (centroid[0] + shift_1, centroid[1] + shift_2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA,
                )
            cv2.putText(
                frame,
                str(label),
                centroid,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

        return frame

    def save_imgs(self, imgs, folder):
        raise NotImplementedError
        for label, img in imgs.items():
            filename = f"{label}-{datetime.now()}.jpeg"
            state = self.detector.parking_status.get(label)
            if state is None:
                continue
            elif state == 1:
                path = os.path.join(folder, "occupied")
            elif state == 0:
                path = os.path.join(folder, "empty")
            self.save_img(img, path, filename)

    @staticmethod
    def save_img(img, folder, filename):
        if img is None:
            return
        path = os.path.join(folder, filename)
        cv2.imwrite(path, img)

    @staticmethod
    def img_is_same(
        first_image_hist, second_image_hist, minimum_commutative_image_diff=1
    ):
        if first_image_hist is None and second_image_hist is None:
            return True
        if first_image_hist is None or second_image_hist is None:
            return False
        img_hist_diff = cv2.compareHist(
            first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA
        )
        img_template_probability_match = cv2.matchTemplate(
            first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED
        )[0][0]
        img_template_diff = 1 - img_template_probability_match

        image_diff = (img_hist_diff / 10) + img_template_diff
        if image_diff < minimum_commutative_image_diff:
            return True
        return False

    @staticmethod
    def get_hist(image):
        if image is None:
            return None
        return cv2.calcHist([image], [0], None, [256], [0, 256])

    def get_labeled_imgs(self, frame):
        imgs = dict()
        if frame is None:
            return imgs
        for label, rect in self.bounds.items():
            imgs[label] = frame[
                rect[0][1] : rect[0][1] + rect[1][1],
                rect[0][0] : rect[0][0] + rect[1][1],
            ]
        return imgs

    def get_changed_labeled_imgs(self, frame, coeff: float = 0.5):

        labeled_imgs = self.get_labeled_imgs(frame)
        doesnt_changed = []
        for label, img in labeled_imgs.items():
            hist = self.get_hist(img)
            if self.img_is_same(hist, self._hists.get(label, None), coeff):
                doesnt_changed.append(label)
            self._hists[label] = hist
        for label in doesnt_changed:
            del labeled_imgs[label]
        return labeled_imgs

    def get_changed_image_after_stabilized(self, frame, coeff: float = 0.5):
        changed_imgs = self.get_changed_labeled_imgs(frame, coeff)
        if changed_imgs:
            self.changed = 1
            return {}
        elif self.changed:
            self.changed = 0
            return self.get_labeled_imgs(frame)
