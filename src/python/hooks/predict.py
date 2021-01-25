import cv2

import detectron2
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

from PyQt5 import QtCore

class Masks:
	def __init__(self, image: str, out_dir: str, model: str):
		"""
		image is a path
		"""
		self.image = image
		self.out_dir = out_dir
		self.model = model

	def predict(self):
		cfg = get_cfg()
		cfg.MODEL.DEVICE='cpu'
		cfg.OUTPUT_DIR = self.out_dir
		cfg.merge_from_file(model_zoo.get_config_file(self.model))
		cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
		cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(self.model)
		predictor = DefaultPredictor(cfg)
		im = cv2.imread(self.image)
		outputs = predictor(im)
		visual = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
		mask = visual.draw_instance_predictions(outputs["instances"].to("cpu"))

		return mask



