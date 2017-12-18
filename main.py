# coding=utf8
# 反應以0.8秒為基準，依此做正確率的學習

import time
import random

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
par = 0.3
dictionary = {
    'iu': 'q',
    'ia': 'w',
    'ua': 'w',
    'er': 'r',
    'uan': 'r',
    'ue': 't',
    'uai': 'y',
    'ü': 'y',
    'sh': 'u',
    'ch': 'i',
    'uo': 'o',
    'un': 'p',
    'iong': 's',
    'ong': 's',
    'uang': 'd',
    'iang': 'd',
    'en': 'f',
    'eng': 'g',
    'ang': 'h',
    'an': 'j',
    'ao': 'k',
    'ai': 'l',
    'ing': ';',
    'ei': 'z',
    'ie': 'x',
    'iao': 'c',
    'zh': 'v',
    'ui': 'v',
    'ou': 'b',
    'in': 'n',
    'ian': 'm',
}
dictionary_eng_ind = [v for v in dictionary]
# dictionary_eng_ind = dictionary
correct_rate = [[[0.01, 1] for i in range(0, 31)], # correct rate, number, 
                [0.01 for i in range(0, 31)],      # correct rate
                [0.01 for i in range(0, 31)],      # correct rate
                [0.01 for i in range(0, 31)],      # correct rate
                [0.01 for i in range(0, 31)]]      # correct rate
p_array = [0.0 for i in range(0, 31)]              # probability weight array

cjd = {}

random.seed()

def read_record():
    file_open_success = False
    try:
        f = open("record.splm", "r")
        file_open_success = True
        f.close()
    except:
        print("檔案 record.splm 不存在！")
        
    if file_open_success:
        print("讀取 record.splm...")
        f = open("record.splm", "r")
        x = f.read()
        x = x.split()
        for i in range(0, 31):
            correct_rate[0][i][0] = float(x[i * 2])
            correct_rate[0][i][1] = int(x[i * 2 + 1])
        for i in range(1, 5):
            for j in range(0, 31):
                correct_rate[i][j] = float(x[62 + 31 * (i - 1) + j])
        f.close()
    else:
        save_record()

def save_record():
    f = open("record.splm", "w")
    for i in range(31):
        f.write(f"{correct_rate[0][i][0]:.9f}" + "\n")
        f.write(str(correct_rate[0][i][1]) + "\n")
    for i in range(1, 5):
        for j in range(0, 31):
            f.write(f"{correct_rate[i][j]:.9f}" + "\n")
    f.close()

def gen_p_array():
    for i in range(0, 31):
        p_array[i] = correct_rate[0][i][0]
        p_array[i] = p_array[i] * (1 - par) + correct_rate[1][i] * par
        p_array[i] = p_array[i] * (1 - par) + correct_rate[2][i] * par
        p_array[i] = p_array[i] * (1 - par) + correct_rate[3][i] * par
        p_array[i] = p_array[i] * 0.5 + correct_rate[4][i] * 0.5
        p_array[i] = 1 / (p_array[i] * 3.14159)
        if i != 0:
            p_array[i] = p_array[i - 1] + p_array[i]

def print_grade():
    for i in range(0, 31):
        p_array[i] = correct_rate[0][i][0]
        p_array[i] = p_array[i] * (1 - par) + correct_rate[1][i] * par
        p_array[i] = p_array[i] * (1 - par) + correct_rate[2][i] * par
        p_array[i] = p_array[i] * (1 - par) + correct_rate[3][i] * par
        p_array[i] = p_array[i] * 0.5 + correct_rate[4][i] * 0.5
        # print(dictionary_eng[dictionary_eng_ind[i]] + "：" + str(p_array[i]))
        if i != 0:
            p_array[i] += p_array[i - 1]
    print("學習成果：", round(p_array[30] / 31 * 100, 2))
    print("建議分數： 80")

def update_record(ind, correct, time):
    correct_rate[0][ind][0] = correct_rate[1][ind] / correct_rate[0][ind][1] + correct_rate[0][ind][0] * (correct_rate[0][ind][1] - 1) / correct_rate[0][ind][1]
    correct_rate[0][ind][1] = correct_rate[0][ind][1] + 1
    for i in range(1, 4):
        correct_rate[i][ind] = correct_rate[i + 1][ind]
    correct_rate[4][ind] = correct * 0.8 / time
    
def get_index():
    rand_num = random.random()
    gen_p_array()
    rand_num = rand_num * p_array[30]
    for i in range(0, 31):
        if rand_num <= p_array[i]:
            return i
    return 30
    
def main_loop():
    print("輸入任意數字或符號來離開程式")
    print("若使用 ctrl+c 離開程式，記錄將不會被保存")
    while True:
        ind = get_index()
        print("=========================")
        print("拼音碼：" + dictionary_eng_ind[ind])
        start_time = time.time()
        x = input("請輸入對應的英文字母：")
        end_time = time.time()
        x = x.lower()
        if (x < 'a' or x > 'z') and x != '' and x != ';':
            print("儲存記錄...")
            save_record()
            print_grade()
            break
        if x == dictionary[dictionary_eng_ind[ind]]:
            time_diff = end_time - start_time
            print(OKGREEN + "正確" + ENDC + "！花費時間：", round(time_diff, 3), "秒")
            update_record(ind, 1.0, time_diff)
        else:
            x = input(FAIL + "錯誤" + ENDC + "！正確答案為：" + FAIL + BOLD + dictionary[dictionary_eng_ind[ind]] + ENDC + "! 按下enter來繼續...")
            update_record(ind, 0.0, 1.0)
            

read_record()
main_loop()
