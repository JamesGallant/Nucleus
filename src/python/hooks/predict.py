import detectron2
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

from PyQt5 import QtCore

class Masks:
	def __init__(self, image):
		self.image = image

	def predict(self):
		cfg = get_cfg()
		cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
		cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
		cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
		predictor = DefaultPredictor(cfg)
		outputs = predictor(self.image)
		visual = Visualizer(self.image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
		mask = visual.draw_instance_predictions(outputs["instances"].to("cpu"))

		return mask



