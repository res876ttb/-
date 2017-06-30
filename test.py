import sys
import random

cjd = {}
keys = []
file_path = "newcj.txt"

def read_cj():
	file_open_success = False
	try: 
		f = open(file_path, "r")
		file_open_success = True
		f.close()
	except: 
		print("檔案 newcj.txt 不存在！")
		sys.exit(1)
	
	if file_open_success:
		f = open(file_path, "r")
		print("讀取 newcj.txt ...")
		
		x = f.read()
		x = x.split()
		length = len(x)
		
		for i in range(0, length, 2):
			cjd[x[i]] = x[i + 1]
		
		keys = list(cjd.keys())
		
		print("讀取完成！")

def getKeys():
	

random.seed()
read_cj()
