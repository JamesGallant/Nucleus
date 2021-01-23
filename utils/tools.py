import os

def _renaming_convention(filenumber: int):
	"""
	takes a pointer and converts it to a filename
	param: file number is the pointer
	returns name
	#O(1)ST
	"""
	if filenumber < 10:
		return f"000{filenumber}"
	elif filenumber < 100:
		return f"00{filenumber}"
	elif filenumber < 1000:
		return f"0{filenumber}"
	else:
		return filenumber


def rename(directory: str):
	"""
	params: directory location
	returns null
	renames all files in a directory using counts
	renaming is O(logN)
	"""
	if directory == "":
		raise AssertionError("Provide a file location")

	files = os.listdir(directory) 
	left = 0
	right = len(files) - 1

	while left < right:
		os.rename(os.path.join(directory, files[left]), os.path.join(directory, f"{_renaming_convention(left)}.png"))
		os.rename(os.path.join(directory, files[right]), os.path.join(directory, f"{_renaming_convention(right)}.png"))
		left += 1
		right -= 1


