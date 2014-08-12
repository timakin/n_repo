# coding:utf-8
import sys
import re
import csv
import time
import read_result_of_wos_list as rrw

adv_degree = open('author_list/advisor_degree_raw.csv', 'rb')
wos_list   = open('wos_list.csv', 'aw')
fileReader = csv.reader(adv_degree)
fileWriter = csv.writer(wos_list)

def create_wos_plain_list():
	for row in fileReader:
		if row[0] == "f_id": 
			continue
		else:
			for year in range(1960, 2015):
				fileWriter.writerow([row[0], year, row[4], row[1], 0, 0])

if __name__ == '__main__':
	create_wos_plain_list()
