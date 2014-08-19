# coding:utf-8
# 著者のステータスが論文のものと合致しているかチェックするスクリプト
import re
import os
import import_author_list as im
import write_to_wos_result as wtwr
from institution_list import inst_list as inst_list
from should_excluded_institution import black_list as black_list
from list_for_f_dep import f_dep_dict as fdep_dict
from collections import OrderedDict

record_num       = 0
year_NA_flag     = {}
dict_for_author  = {}
imported_dict    = im.return_author_list(dict_for_author)
full_match       = {}
af_tokyo         = {}
af_phys          = {}
af_tokyo_dep     = {}
py_match         = {}
author_dep       = {}
dep_units        = {}
dep_match        = {}
dep_list         = {}
unique_dep_list  = []
tmp_dep          = {}

def return_conditions(target={}, author_dict={}, text_name='', paper_index=0):
  # 著者の名前によるマッチング==========================
  if author_dict['faculty_name'].upper() not in target['AU'].upper():
    print "イニシャルが一致しません"
    return
  else:
    print "AUが一致しました"
    if author_dict['full_name'].upper() not in target['AF'].upper() and author_dict['faculty_name'].upper() not in target['AF']:
      print "名前が正しく有りません"
      return
    elif author_dict['full_name'].upper() in target['AF'].upper():
      print "フルネームが一致しました"
      full_match[paper_index] = 1  
    elif author_dict['faculty_name'].upper() in target['AF'].upper():
      print "イニシャルがAFと一致しました"
      full_match[paper_index] = 0

    # 著者の所属によるマッチング==========================
    if target['C1'] == None or ( (not re.search('UNIV TOKYO', target['C1'].upper())) and (not re.search('UNIV TOKYO', str(target['RP']).upper())) ):
      print "東京大学じゃありませんでした"
      return
    else:
      print "東京大学でした"
      af_tokyo[paper_index] = 1
      if re.search('UNIV TOKYO, DEPT PHYS', target['C1'].upper()):
        print "物理学科でした"
        af_phys[paper_index] = 1
        af_tokyo_dep[paper_index] = 'DEPT PHYS'
      else:
        print "物理学科じゃありません"
        tmp_dep[paper_index] = stock_dep(target['C1'].upper())
        af_tokyo_dep[paper_index] = delete_dep(tmp_dep[paper_index])
        if not af_tokyo_dep[paper_index]:
          return
        af_phys[paper_index] = 0

      # 論文執筆の時期によるマッチング==========================
      year_NA_flag[paper_index] = 0
      if author_dict['start_year'] is '' or author_dict['end_year'] is '':
        author_dict['start_year'] = 'NA'
        author_dict['end_year'] = 'NA'
        year_NA_flag[paper_index] = 1
      elif 'LC' in author_dict['start_year']:
        author_dict['start_year'] = '1965'
      elif 'RC' in author_dict['end_year']:
        author_dict['end_year']   = '2015'
      
      if not year_NA_flag[paper_index]:
        time_span = range(int(author_dict['start_year']), int(author_dict['end_year']))
        
      # 著者が研究機関に所属した間に当該論文が出稿されたかのチェック==========================
      if int(target['PY']) not in time_span:
        print "所属期間内に論文が出ていません"
        return
      else:
        print "所属期間内に論文がでました"
        py_match[paper_index] = 1

        # 執筆されたタイミングで著者の所属機関が論文の在籍者の所属期間と一致するかのチェック==========================
        print "Author_dict['dep'] : "+author_dict['dep']
        if author_dict['dep'] == '':
          print "Author_dictが空です。"
          dep_units[paper_index] = None
          dep_match[paper_index] = 'NA' # 所属期間がマッチしたか如何ではなく、データの有無で判別する場合はNA
        else:
          for unit_string in author_dict['dep']:
            for row in fdep_dict:
              if row[0] is unit_string:
                for unit_dep in row[1]:
                  if af_tokyo_dep[paper_index] == unit_dep:
                    dep_match[paper_index] = 1
                    print "所属期間がマッチしました。"
                  else:
                    dep_match[paper_index] = None         
     
        if dep_match[paper_index] == None:
          print "論文執筆時の所属機関が不適切です"
          return
        else:
          print "論文執筆時の所属機関が適切です"

  if af_tokyo[paper_index] and py_match[paper_index] and (dep_match[paper_index] != None):
    global record_num
    record_num = record_num + 1

    tf=open('result_texts/results_'+author_dict['faculty_name']+'.txt','a')
    tf.write('\n') 
    tf.write('\n') 
    tf.write('==================================================\n') 
    tf.write('\n') 
    tf.write('\n') 
    tf.write('\n')
    tf.write('RECORD_NUM   =>'+str(record_num)+'\n')
    tf.write('FACULTY_NAME =>'+author_dict['faculty_name']+'\n')
    tf.write('F_ID         =>'+author_dict['id']+'\n')
    tf.write('FULL_MATCH   =>'+str(full_match[paper_index])+'\n')
    tf.write('AF_TOKYO     =>'+str(af_tokyo[paper_index])+'\n')
    tf.write('AF_TOKYO_DEP =>'+str(af_tokyo_dep[paper_index])+'\n')
    tf.write('AF_PHYS      =>'+str(af_phys[paper_index])+'\n')
    tf.write('PY_MATCH     =>'+str(py_match[paper_index])+'\n')
    tf.write('DEP_MATCH    =>'+str(dep_match[paper_index])+'\n')
    tf.write('PY           =>'+target['PY']+'\n')
    tf.write('PT           =>'+target['PT']+'\n')
    tf.write('SO           =>'+target['SO']+'\n')
    tf.write('TI           =>'+target['TI']+'\n')
    tf.write('RP           =>'+str(target['RP']).upper()+'\n')
    tf.write('FILE_NAME    =>'+str(text_name)+'\n')
    tf.write('PAPER_ID     =>'+str(paper_index)+'\n')
    tf.close()

    # wos_result.csvにその年の著者の論文出稿数の単純和と、インパクトファクターを書き込む
    # その後、wos_list.csvとwos_result.csvの内容を一致させる
    wtwr.write_to_wos_result(author_dict['id'], target['PY'], target['SO'])
    os.system('python copy_result_to_list.py')

    # unique_list（学科のリスト）を作成する
    if type(af_tokyo_dep[paper_index])==str:
      unique_dep_list.append(af_tokyo_dep[paper_index])
    else:
      for i in af_tokyo_dep[paper_index]:
        unique_dep_list.append(i)

def stock_dep(target_c1=''):
  dep_list  = []
  listed_c1 = target_c1.replace('.;', ',').split(',')
  for i,line in enumerate(listed_c1):
    if line.find("UNIV TOKYO") >= 0:
      for x in inst_list:
        if x in listed_c1[i+1]:
          dep_list = listed_c1[i+1].lstrip().lstrip()
  return dep_list

def delete_dep(dep_list=[]):
  for i,line in enumerate(dep_list):
    for x in black_list:
      if x == dep_list:
        dep_list = []
  return dep_list
        
