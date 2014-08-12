# coding:utf-8
import sys
import re
import csv

def read_wos_list():
  wos_list = open('wos_list.csv', 'rb')
  result_file = csv.reader(wos_list)
  for row in result_file:
    print row

if __name__ == '__main__':
  read_wos_list()
