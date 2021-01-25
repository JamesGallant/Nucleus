import unittest, os
import detectron2
import cv2
import numpy as np
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog


from src.python.hooks.predict import Masks

MODELS = ["COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"]
TESTING_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(TESTING_DIR, "test_resources", "images")

def predict_image(image):
	cfg = get_cfg()
	cfg.MODEL.DEVICE='cpu'
	cfg.OUTPUT_DIR = os.path.join(TESTING_DIR, "test_resources", "models")
	cfg.merge_from_file(model_zoo.get_config_file(MODELS[0]))
	cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
	cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(MODELS[0])
	predictor = DefaultPredictor(cfg)
	im = cv2.imread(image)
	outputs = predictor(im)
	visual = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
	mask = visual.draw_instance_predictions(outputs["instances"].to("cpu"))

	return mask.get_image()

def prediction_from_nucleus(image):
	mask = Masks(image=image, out_dir=os.path.join(TESTING_DIR, "test_resources", "models"), model = MODELS[0])
	predicted_mask = mask.predict()
	return predicted_mask.get_image()


def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

class Testrunner(unittest.TestCase):
	def test_predict(self):
		prediction_test = []
		prediciton_nucleus = []

		for images in os.listdir(IMAGES_DIR):
			im = os.path.join(TESTING_DIR, "test_resources", "images", images)
			prediction_test.append(predict_image(image=im))
			prediciton_nucleus.append(prediction_from_nucleus(image=im))

		out = is_similar(prediction_test[0], prediciton_nucleus[0])

		self.assertEqual(prediction_test[0].shape, prediciton_nucleus[0].shape)


		
if __name__ == '__main__':
	unittest.main()