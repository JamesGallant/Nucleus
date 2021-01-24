import qdarkstyle
import sys, os
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore

from src.python.hooks.predict import Masks

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.root = os.path.dirname(os.path.abspath(__file__))

		if "data" not in os.listdir(self.root):
			os.makedirs(os.path.join(self.root, "data", "train"), exist_ok=True)
			os.makedirs(os.path.join(self.root, "data", "val"), exist_ok=True)
			os.makedirs(os.path.join(self.root, "data", "test"), exist_ok=True)

		self.gui_metadata = {
		"current_image": None,
		"placeholder1": os.path.join(self.root, "src", "resources", "placeholder1.png"),
		"placeholder2": os.path.join(self.root, "src", "resources", "placeholder2.png")
		}

		self.accepted_formats = [".png", ".tiff", ".jpeg", ".jpg"]
		self.initiateUI()

	
	def initiateUI(self):
		QtWidgets.QToolTip.setFont(QtGui.QFont('Times New Roman', 12))
		central_widget = QtWidgets.QWidget()

		self.setWindowTitle("Nucleus: GUI interface to Facebook's Detectron2")
		self.setCentralWidget(central_widget)

		# dynamic widgets
		self.menubar()
		self.toolbar()

		layout = QtWidgets.QGridLayout(central_widget)
		layout.addWidget(self.display(), 0, 0)
		
		# permanent widgets
		self.progressbar = QtWidgets.QProgressBar()
		self.progressbar.setMaximum(100)
		self.progressbar.setValue(0)
		self.statusBar().addPermanentWidget(self.progressbar)

		self.showMaximized()
		self.show()


	def menubar(self):
		 menu = self.menuBar()
		 # file 
		 filemenu = menu.addMenu('File')

		 import_files = QtWidgets.QAction("Import", self)
		 import_files.setShortcut("Ctrl+I")

		 export_files = QtWidgets.QAction("Export", self)
		 export_files.setShortcut("Ctrl+E")

		 predict_mask = QtWidgets.QAction("Predict", self)
		 predict_mask.setShortcut("Ctrl+P")
		 predict_mask.triggered.connect(self.predict_mask)

		 filemenu.addAction(import_files)
		 filemenu.addAction(export_files)
		 filemenu.addAction(predict_mask)

		 # resources
		 resourcemenu = menu.addMenu('Resources')

		 via = QtWidgets.QAction('Annotator', self)
		 detectron2 = QtWidgets.QAction('Detectron2', self)


		 resourcemenu.addAction(via)
		 resourcemenu.addAction(detectron2)

	def toolbar(self):
		pass


	def display(self):
		groupBox = QtWidgets.QGroupBox()
		grid = QtWidgets.QGridLayout()

		# display file
		self.image_holder_base = QtWidgets.QLabel()
		self.image_holder_base.setPixmap(QtGui.QPixmap(self.gui_metadata.get("placeholder1")))
		self.image_holder_base.setScaledContents(True)

		self.image_holder_mask = QtWidgets.QLabel()
		self.image_holder_mask.setPixmap(QtGui.QPixmap(self.gui_metadata.get("placeholder2")))
		self.image_holder_mask.setScaledContents(True)
		
		# file browser
		self.filesystem = QtWidgets.QTreeView()
		self.filesystem.setFixedSize(680, 1020)
		model = QtWidgets.QFileSystemModel()
		model.setRootPath(os.path.join(self.root, "data"))
		self.filesystem.setModel(model)
		self.filesystem.doubleClicked.connect(self.show_image)

		
		grid.addWidget(self.filesystem, 0,0,0,1)
		grid.addWidget(self.image_holder_base, 0,1)
		grid.addWidget(self.image_holder_mask, 1,1)
		groupBox.setLayout(grid)

		return groupBox

	def show_image(self, signal):
		file_path=self.filesystem.model().filePath(signal)
		self.gui_metadata["current_image"] = file_path

		file_extension = os.path.splitext(file_path)[1]


		if file_extension not in self.accepted_formats:
			QtWidgets.QMessageBox.about(self, "Error", f"Please choose one of the following formats: {[items for items in self.accepted_formats]}")
			return None
		
		image_base = cv2.imread(file_path)
		image_mask = cv2.imread(file_path)

		base_image_display = QtGui.QImage(image_base.data, image_base.shape[1], image_base.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
	
		mask_image_display = QtGui.QImage(image_mask.data, image_mask.shape[1], image_mask.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
	
		self.image_holder_base.setPixmap(QtGui.QPixmap.fromImage(base_image_display))
		self.image_holder_mask.setPixmap(QtGui.QPixmap.fromImage(mask_image_display))


	def predict_mask(self):
		image = self.gui_metadata.get("current_image")
		mask = Masks(image=image)
		cv2.imshow(mask.get_image()[:, :, ::-1])



def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    gui = MainWindow()
    app.exec_()
    sys.exit()

if __name__ == '__main__':
	main()