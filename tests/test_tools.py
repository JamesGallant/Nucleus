import unittest
import shutil
import os

from utils import tools

class RenameTest:
	def __init__(self, filecount):
		self.filecount = filecount
		self.dummy_directory = os.path.join(os.getcwd(), "tests", "datatest")

	def create_dummy_dir(self):
		os.mkdir(self.dummy_directory)

	def create_dummy_files(self):
		for item in range(0, self.filecount):
			open(os.path.join(self.dummy_directory, f"file-{item}.txt"), mode='w+').close()

	def remove_dummy_files(self):
		shutil.rmtree(self.dummy_directory)

	def get_dir_contents(self):
		return os.listdir(self.dummy_directory)

	def main(self):
		self.create_dummy_dir()
		self.create_dummy_files()
		tools.rename(self.dummy_directory)
		contents_renamed = self.get_dir_contents()
		self.remove_dummy_files()
		return contents_renamed






class Testrunner(unittest.TestCase):
	def test_rename1(self):
		Rename = RenameTest(filecount=10)
		correct_names = [f"000{items}.png" for items in range(10)]
		self.assertEqual(Rename.main(), correct_names)
		
if __name__ == '__main__':
	unittest.main()