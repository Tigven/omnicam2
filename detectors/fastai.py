import torchvision.transforms as transforms
from fastai.conv_learner import *
from fastai.dataset import *
from fastai.plots import *

from .basic import Detector


class FastAIDetector(Detector):
    def __init__(self, arch, size, path, model, parking_data):
        PATH = path
        self.sz = size
        if arch == 'resnet34':
            arch = resnet34
        elif arch == 'resnet18':
            arch = resnet18
        data = ImageClassifierData.from_paths(
            PATH, bs=24, tfms=tfms_from_model(arch, self.sz))
        self.learn = ConvLearner.pretrained(arch, data, precompute=False)
        self.learn.load(model)

        self.composed = transforms.Compose([
            transforms.Resize(self.sz),
            transforms.CenterCrop(self.sz),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def detect(self, imgs):
        status = {}
        imgs_ar = np.zeros((len(imgs), 3, self.sz, self.sz))
        labels = []
        i = 0
        for label, img in imgs.items():
            img = Image.fromarray(img)
            imgs_ar[i] = np.asarray(self.composed(img))
            labels.append(label)
            i += 1
        preds = self.learn.predict_array(imgs_ar)
        for i, pred in enumerate(preds):
            status[labels[i]] = np.argmax(pred)
        return status
