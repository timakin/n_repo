#! /usr/bin/env python
# -*- coding:utf-8 -*-
import csv
import re
from collections import OrderedDict
def return_author_list(author_dict={}):
	with open('author_list/advisor_degree_raw.csv', 'r') as f:
		i=-1
		reader = csv.reader(f)
		for row in reader:
			for x in row:
				unicode(x, 'utf-8')
			author_dict[i] =	{'id': row[0], 'full_name': row[4].upper().replace(' ',', '), 'faculty_name': row[7].upper().replace(' ',', '), 'raw_name': row[7], 'start_year': row[8], 'end_year': row[9]}
			i=i+1
	del author_dict[-1]
	return author_dict

if __name__ == '__main__':
	author_dict={}
	author = return_author_list(author_dict)
	print author
