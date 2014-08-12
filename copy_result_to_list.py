#! /usr/bin/env python
# -*- coding:utf-8 -*-
import csv
import re
import shutil
import os

def copy_result_to_list():
  if os.path.exists('wos_list.csv'):
    os.remove('wos_list.csv') 
  wos_list3 = open('wos_result.csv', 'rb')
  read_written = csv.reader(wos_list3)
  wos_list4 = open('wos_list.csv', 'aw')
  copy_written = csv.writer(wos_list4)

  i = 0
  for row in read_written:
    print str(i) + 'copy中'
    row_list = [row[0], row[1], row[2], row[3], row[4], row[5]]
    print row_list
    copy_written.writerow([row[0], row[1], row[2], row[3], row[4], row[5]])
    i = i+1

if __name__ == '__main__':
  copy_result_to_list()
