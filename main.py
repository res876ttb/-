# coding=utf8
# 反應以0.8秒為基準，依此做正確率的學習

import time
import random

dictionary_eng = {'a': '日', 'b': '月', 'c': '金', 'd': '木', 'e': '水', 'f': '火', 'g': '土', 'h': '竹', 'i': '戈', 'j': '十', 'k': '大', 'l': '中', 'm': '一', 'n': '弓', 'o': '人', 'p': '心', 'q': '手', 'r': '口', 's': '尸', 't': '廿', 'u': '山', 'v': '女', 'w': '田', 'x': '重', 'y': '卜', 'z': '難'}
dictionary_eng_ind = [v for v in dictionary_eng]
correct_rate = [[[0.01, 1] for i in range(0, 26)], # correct rate, number, 
				[0.01 for i in range(0, 26)],      # correct rate
				[0.01 for i in range(0, 26)],      # correct rate
				[0.01 for i in range(0, 26)],      # correct rate
				[0.01 for i in range(0, 26)]]      # correct rate
p_array = [0.0 for i in range(0, 26)]             # probability weight array

random.seed()

def read_record():
	file_open_success = False
	try:
		f = open("record.cjlm", "r")
		file_open_success = True
		f.close()
	except:
		print("檔案 record.cjlm 不存在！")
		
	if file_open_success:
		print("讀取 record.cjlm...")
		f = open("record.cjlm", "r")
		x = f.read()
		x = x.split()
		for i in range(0, 26):
			correct_rate[0][i][0] = float(x[i * 2])
			correct_rate[0][i][1] = int(x[i * 2 + 1])
		for i in range(1, 5):
			for j in range(0, 26):
				correct_rate[i][j] = float(x[52 + 26 * (i - 1) + j])
		f.close()
	else:
		save_record()

def save_record():
	f = open("record.cjlm", "w")
	for i in range(26):
		f.write(f"{correct_rate[0][i][0]:.9f}\n")
		f.write(str(correct_rate[0][i][1]) + "\n")
	for i in range(1, 5):
		for j in range(0, 26):
			f.write(f"{correct_rate[i][j]:.9f}\n")
	f.close()

def gen_p_array():
	par = 0.4
	for i in range(0, 26):
		p_array[i] = correct_rate[0][i][0]
		p_array[i] = p_array[i] * (1 - par) + correct_rate[1][i] * par
		p_array[i] = p_array[i] * (1 - par) + correct_rate[2][i] * par
		p_array[i] = p_array[i] * (1 - par) + correct_rate[3][i] * par
		p_array[i] = p_array[i] * (1 - par) + correct_rate[4][i] * par
		p_array[i] = 1 / p_array[i]
		if i != 0:
			p_array[i] = p_array[i - 1] + p_array[i]

def update_record(ind, correct, time):
	correct_rate[0][ind][0] = correct_rate[1][ind] / correct_rate[0][ind][1] + correct_rate[0][ind][0] * (correct_rate[0][ind][1] - 1) / correct_rate[0][ind][1]
	correct_rate[0][ind][1] = correct_rate[0][ind][1] + 1
	for i in range(1, 4):
		correct_rate[i][ind] = correct_rate[i + 1][ind]
	correct_rate[4][ind] = correct * 0.8 / time
	
def get_index():
	rand_num = random.random()
	gen_p_array()
	rand_num = rand_num * p_array[25]
	for i in range(0, 26):
		if rand_num <= p_array[i]:
			return i
	return 25
	
def main_loop():
	print("輸入任意數字或符號來離開程式")
	print("若使用ctrl+c離開程式，記錄將不會被保存")
	while True:
		ind = get_index()
		print("=========================")
		print("倉頡碼：" + dictionary_eng[dictionary_eng_ind[ind]])
		start_time = time.time()
		x = input("請輸入對應的英文字母：")
		end_time = time.time()
		x = x.lower()
		if (x < 'a' or x > 'z') and x != '':
			print("儲存記錄...")
			save_record()
			break
		if x == dictionary_eng_ind[ind]:
			time_diff = end_time - start_time
			print("正確！花費時間：", round(time_diff, 3), "秒")
			update_record(ind, 1.0, time_diff)
		else:
			print("錯誤！正確答案為：" + dictionary_eng_ind[ind])
			update_record(ind, 0.0, 1.0)

read_record()
main_loop()
