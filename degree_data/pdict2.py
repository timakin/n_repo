# coding:utf-8
import re
import inspect
from collections import OrderedDict

frame = inspect.currentframe()
pattern_AU = re.compile('\nAU .+?\n   ')
pattern_AF = re.compile('\nAF .+?\n   ')
pattern_TI = re.compile('\nTI .+?\n   ')
pattern_C1 = re.compile('\nC1 .+?\n   ')
pattern_CR = re.compile('\nCR .+?\n   ')
pattern_WC = re.compile('\nWC .+?\n   ')
pattern_SC = re.compile('\nSC .+?\n   ')

KEYS=[
'PT',
'AU',
'AF',
'CA',
'TI',
'ED',
'SO',
'SE',
'BS',
'LA',
'DT',
'CT',
'CY',
'HO',
'CL',
'SP',
'DE',
'ID',
'AB',
'C1',
'RP',
'EM',
'FU',
'FX',
'CR',
'NR',
'TC',
'PU',
'PI',
'PA',
'SC',
'SN',
'BN',
'J9',
'JI',
'PD',
'PY',
'VL',
'IS',
'PN',
'SU',
'SI',
'BP',
'EP',
'AR',
'PG',
'DI',
'SC',
'WC',#omitted
'GA',
'UT',
'PT_LINE',
]

def return_paper_dict(textfile):
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
		for i in plist:#debug
			print
			print
			print
			print '==================================THIS IS THE START OF LIST=========================='
			# ここから辞書の個別要素をプリント
			for d in i:
				print d,'=>',i[d]
			# このタイミングで個別の辞書リストの表示が終了する
			# ここで条件設定をして、要件を満たすメソッドを実行すれば良いのでは？
			# iをdictとして受け取り、それに対して処理を実行してみる。
			print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<START OF CHECK CONDITIONS<<<<<<<<<<<<<<<<<<<<<<<<'
			print f
			check_conditions(i, author_dict, textfile)
			print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>END OF CHECK CONDITIONS>>>>>>>>>>>>>>>>>>>>>>>>'
			print '==================================THIS IS THE END OF LIST=========================='
	return plist


author_dict = {'id': 1,'faculty_name': 'AKIYAMA, H','full_name': 'AKIYAMA, H','start_year': 1962,'end_year': 2022}
full_match = {}
af_tokyo = {}
af_phys = {}
af_tokyo_dep = {}
py_match = {}

def check_conditions(target={}, author_dict={}, text_name=''):
	print author_dict
	if author_dict['faculty_name'] not in target['AU']:
		return
	else:
		print "第１チェック"
		if author_dict['full_name'] not in target['AF']:
			return
		else:
			print "第２チェック"
			full_match[author_dict['id']] = 1
			if target['C1'] == None or re.search('Univ Tokyo', target['C1']):
				return
			else:
				print "第３チェック"
				af_tokyo[author_dict['id']] = 1
				if re.search('Univ Tokyo, Dept Appl Phys', target['C1']):
					af_tokyo_dep[author_dict['id']] = '所属学科'
					print "第４チェック"
				else:
					print "第５チェック"
					af_phys[author_dict['id']] = 1
					af_tokyo_dep[author_dict['id']] = 'DEPT PHYS'
				time_span = range(author_dict['start_year'], author_dict['end_year'])
				if int(target['PY']) not in time_span:
					return
				else:
					print "第６チェック"
					py_match[author_dict['id']] = 1

	if af_tokyo[author_dict['id']] and py_match[author_dict['id']]:
		print 'd(｀･ω´･+)ｬｯﾀﾈ+.☆ﾟ+.☆ﾟ'
		print ('FACULTY_NAME =>', author_dict['faculty_name'])
		print ('F_ID         =>', author_dict['id'])
		print ('FULL_MATCH   =>', full_match[author_dict['id']])
		print ('AF_TOKYO     =>', af_tokyo[author_dict['id']])
		print ('AF_TOKYO_DEP =>', af_tokyo_dep[author_dict['id']])
		print ('AF_PHYS      =>', af_phys[author_dict['id']])
		print ('PY_MATCH     =>', py_match[author_dict['id']])
		print ('PY           =>', target['PY'])
		print ('PT           =>', target['PT'])
		print ('SO           =>', target['SO'])
		print ('TI           =>', target['TI'])
		print ('FILE_NAME    =>', text_name)
		print ('PT_LINE      =>', )

# 実際のチェックでは、次の条件を満たす必要がある
# 1.あらかじめ教員.xlsから、教員の辞書リストを作成しておく
# 2.複数のテキストファイルを開いて、処理を実行できる
# 3.各教員（author_listの各要素）について、check_condititionsを実行する
# 4.値が存在しない場合、for文の次に移るので、returnではなくcontinueにする
# 5.結果を格納しておく辞書を新たに作成する
# 6.PT_LINEを数え上げて入力する

if __name__ == '__main__':
	return_paper_dict('Akiyama H_0_2013-06-13T23:16:19+09:00.txt')
