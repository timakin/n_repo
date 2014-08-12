# coding:utf-8
import sys
import csv
import re
import read_result_of_wos_list as rrw
import create_wos_list as cwl
import write_to_wos_result as wtwr
import time
import os

if __name__ == '__main__':
#  cwl.create_wos_plain_list()
#  time.sleep(10)
#  rrw.read_wos_list()
	wtwr.write_to_wos_result(1,1980, 'COMMUNICATIONS IN MATHEMATICAL PHYSICS')
	os.system('python copy_result_to_list.py')