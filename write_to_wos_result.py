#! /usr/bin/env python
# -*- coding:utf-8 -*-
# インパクトファクターを考慮した計算結果を出力する為のスクリプト
import csv
import re
import shutil
import os
from collections import OrderedDict
import jcrlist3 as jc


def multiple_impact_factor(journal_name=''):
	impact_factor = 0
	for row in jc.jcrlist:
		if journal_name in row[1]:
			impact_factor = row[0]
	return impact_factor


def write_to_wos_result(f_id=0, year=0, target_SO='', year_NA_flag=0, dep_match='', cw=0):
	if os.path.exists('wos_result.csv'):
		os.remove('wos_result.csv')
	wos_list 											= open('wos_result.csv', 'awt')
	fileWriter 										= csv.writer(wos_list)
	wos_list2   									= open('wos_list.csv', 'rb')
	result_file 									= csv.reader(wos_list2)
	if_existed_list 							= open('if_existed_list.csv', 'awt')
	write_to_if_existed_list 			= csv.writer(if_existed_list)
	if_not_existed_list 					= open('if_not_existed_list.csv', 'awt')
	write_to_if_not_existed_list 	= csv.writer(if_not_existed_list)	
	impact_factor 								= multiple_impact_factor(target_SO)

	for row in result_file:
		if row[0] == "f_id":
			continue
		else:
			if (year_NA_flag == 1 or dep_match == "NA"):
				if (row[0] == str(f_id)):
					fileWriter.writerow([row[0], row[1], row[2], row[3], 'NA', 'NA', 'NA'])
				else:
					fileWriter.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
			else:
				if (row[0] == str(f_id) and row[1] == str(year)):
					#ここにNAふらぐについての記述をいれて、上のstr(year)をなんとかする
					fileWriter.writerow([row[0], row[1], row[2], row[3], str(int(row[4])+1), str((float(row[5])+(impact_factor))), str((float(row[6])+(impact_factor*cw)))])
					if impact_factor == 0:
						write_to_if_not_existed_list.writerow([row[1], row[3], str(impact_factor), target_SO])
					else:
						write_to_if_existed_list.writerow([row[1], row[3], str(impact_factor), target_SO])
				else:
					fileWriter.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])


if __name__ == '__main__':
	write_to_wos_result(1, 1990, 'COMMUNICATIONS IN MATHEMATICAL PHYSICS')
