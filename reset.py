import os
import glob

dirs = ['clean_data/*','prod_data/*','figures/*']
for directory in dirs:
	files = glob.glob(directory)
	for f in files:
		os.remove(f)