# coding:utf-8
import sys
import re
import glob
import import_author_list as im
import check_conditions as cc
from collections import OrderedDict
from keys_used_for_pattern_matching import KEYS as KEYS

default_params = sys.argv
start_file_num = default_params[1]
end_file_num   = default_params[2]


pattern_AU = re.compile('\nAU .+?\n   ')
pattern_AF = re.compile('\nAF .+?\n   ')
pattern_TI = re.compile('\nTI .+?\n   ')
pattern_C1 = re.compile('\nC1 .+?\n   ')
pattern_CR = re.compile('\nCR .+?\n   ')
pattern_WC = re.compile('\nWC .+?\n   ')
pattern_SC = re.compile('\nSC .+?\n   ')


def return_paper_dict(textfile, author_dict={}):
	with open(textfile, 'r') as f:
		lines=[]
		for l in f:
			l=l.rstrip()
			lines.append(l)
		al = '\n'.join(lines)
		al = re.sub('FN Thomson Reuters Web of Science.*\nVR 1.0', '', al)
		al = re.sub('\nEF', '', al)
		while re.search(pattern_AU, al):
			al = re.sub('(\nAU .+?)(\n   )', r'\1;', al)
		while re.search(pattern_AF, al):
			al = re.sub('(\nAF .+?)(\n   )', r'\1;', al)
		while re.search(pattern_TI, al):
			al = re.sub('(\nTI .+?)(\n   )', r'\1 ', al)
		while re.search(pattern_C1, al):
			al = re.sub('(\nC1 .+?)(\n   )', r'\1;', al)
		while re.search(pattern_CR, al):
			al = re.sub('(\nCR .+?)(\n   )', r'\1;', al)
		while re.search(pattern_WC, al):
			al = re.sub('(\nWC .+?)(\n   )', r'\1;', al)
		while re.search(pattern_SC, al):
			al = re.sub('(\nSC .+?)(\n   )', r'\1;', al)
		papers = al.split('\nER\n')
		plist =[]
		for i in papers:
			i = re.sub('(\n..)( )',r'\1***', i)
			j = i.split('\n')
			pdict=OrderedDict.fromkeys(KEYS)
			for k in j:
				k = k.split('***')
				if k[0] in pdict.keys():
					pdict[k[0]] = k[1]
			plist.append(pdict)
		del plist[-1]
		# ここから辞書全体の表示が始まる
		for paper_index,i in enumerate(plist):#debug
			print
			print
			print
			# ここから辞書の個別要素をプリント
			for d in i:
				print d,'=>',i[d]
			# このタイミングで個別の辞書リストの表示が終了する
			# ここで条件設定をして、要件を満たすメソッドを実行すれば良いのでは？
			print '======================================='
			cc.return_conditions(i, author_dict, textfile, paper_index)
			print '======================================='
			print
			print
			print
	return plist

#faculty_nameと一致するtxtファイルの配列を返す
#その各要素ごとにreturn_paper_dictを実行する
def return_textfile_lists(a_name=''):
	matched_text_list = []
	for text_name in glob.glob('degree_data/'+a_name+'*.txt'):
		matched_text_list.append(text_name)
	return matched_text_list

if __name__ == '__main__':
	for i in range(int(start_file_num), int(end_file_num)):
		print cc.imported_dict[i]
	 	res = return_textfile_lists(cc.imported_dict[i]['raw_name'])
		print res
		for text_file in res:
			result = return_paper_dict(text_file, cc.imported_dict[i])
	unique_list = cc.unique_dep_list

	list_file = open('unique_list.txt', 'a')
	for x in list(set(unique_list)):
		list_file.write(x+'\n')
	list_file.close()
