# coding:utf-8
# 著者のステータスが論文のものと合致しているかチェックするスクリプト
import re
import os
import import_author_list as im
import write_to_wos_result as wtwr
import contribution_weight as cw
from institution_list import inst_list as inst_list
from should_excluded_institution import black_list as black_list
from list_for_f_dep import f_dep_dict as fdep_dict
from list_for_f_dep import grad_second_dep_list as grad_dep_list
from list_for_f_dep import fac_second_dep_list as fac_dep_list
from list_for_f_dep import liveral_second_dep_list as l_dep_list
from collections import OrderedDict

record_num       = 0
RP_matching_flag = {}
C1_matching_flag = {}
year_NA_flag     = {}
dict_for_author  = {}
imported_dict    = im.return_author_list(dict_for_author)
full_match       = {}
af_tokyo         = {}
af_phys          = {}
# 東京大学に所属していたとして、どの機関だったか。
af_tokyo_dep     = {}

# 所属期間に論文が出ているかどうか
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
    #print "イニシャルが一致しません"
    return
  else:
    #print "AUが一致しました"
    if (author_dict['full_name'].upper() not in target['AF'].upper()) and (author_dict['faculty_name'].upper() not in target['AF'].upper()):
      #print "名前が正しく有りません"
      return
    elif author_dict['full_name'].upper() in target['AF'].upper():
      #print "フルネームが一致しました"
      if (re.search(author_dict['faculty_name'].upper(), str(target['RP']).upper())):
        #print "RP_check1"
        RP_check(str(target['RP']), str(target['C1']), paper_index, af_tokyo, af_phys, af_tokyo_dep, tmp_dep)
        #print "RP_matching_flag: " + str(RP_matching_flag[paper_index])
        if (not RP_matching_flag[paper_index] == 1) and (not C1_matching_flag[paper_index] == 1):
          return
      else:
        #print "C1_check1"
        C1_check(str(target['C1']), paper_index, af_tokyo, af_phys, af_tokyo_dep, tmp_dep)
        #print "C1_matching_flag: " + str(C1_matching_flag[paper_index])
        if (not C1_matching_flag[paper_index] == 1):
          return
      full_match[paper_index] = 1
    elif (author_dict['faculty_name'].upper() in target['AF'].upper()):
      #print "短縮名が一致"
      if (re.search(author_dict['faculty_name'].upper(), str(target['RP']).upper())):
        #print "RP_check2"
        RP_check(str(target['RP']), str(target['C1']), paper_index, af_tokyo, af_phys, af_tokyo_dep, tmp_dep)
        #print "RP_matching_flag: " + str(RP_matching_flag[paper_index])
        if (not RP_matching_flag[paper_index] == 1) and (not C1_matching_flag[paper_index] == 1):
          #print "だみだ"
          return
      else:
        #print "C1_check2"
        C1_check(str(target['C1']), paper_index, af_tokyo, af_phys, af_tokyo_dep, tmp_dep)
        #print "C1_matching_flag: " + str(C1_matching_flag[paper_index])
        if (not C1_matching_flag[paper_index] == 1):
          #print "だみだみだ"
          return
      full_match[paper_index] = 0




    # 論文執筆の時期によるマッチング==========================
    #print "==========="
    #print "AF_TOKYO_DEP: " + af_tokyo_dep[paper_index]
    year_NA_flag[paper_index] = 0
    if author_dict['start_year'] == "" or author_dict['start_year'] == "NA" or author_dict['end_year'] == "" or author_dict['end_year'] == "NA":
      author_dict['start_year'] = 'NA'
      author_dict['end_year'] = 'NA'
      year_NA_flag[paper_index] = 1
    #  print "NAでだめですた"
      wtwr.write_to_wos_result(author_dict['id'], target['PY'], target['SO'], year_NA_flag[paper_index])
      os.system('python copy_result_to_list.py')
      return
    elif 'LC' in author_dict['start_year']:
      author_dict['start_year'] = '1965'
    elif 'RC' in author_dict['end_year']:
      author_dict['end_year']   = '2015'
    
    if year_NA_flag[paper_index] == 0:
    #  print "TimeSpanはとりますた"
      time_span = range(int(author_dict['start_year']), int(author_dict['end_year'])+1)

    # 著者が研究機関に所属した間に当該論文が出稿されたかのチェック==========================
    if int(target['PY']) not in time_span:
    #  print "所属期間内に論文が出ていません"
      py_match[paper_index] = 0
    #  print "TARGET_PY: " + target['PY']
    #  print time_span
    #  print "TARGET_TI: " + target['TI']
      return
    else:
    #  print "所属期間内に論文がでました"
      py_match[paper_index] = 1
      # 執筆されたタイミングで著者の所属機関が論文の在籍者の所属期間と一致するかのチェック==========================
      #print "Author_dict['dep'] : "+author_dict['dep']
      if author_dict['dep'] == "" or author_dict['dep'] == "NA":
        #print "Author_dictが空です。"
        dep_units[paper_index] = None
        dep_match[paper_index] = 'NA' # 所属期間がマッチしたか如何ではなく、データの有無で判別する場合はNA
        wtwr.write_to_wos_result(author_dict['id'], target['PY'], target['SO'], year_NA_flag[paper_index], dep_match[paper_index])
        os.system('python copy_result_to_list.py')
        return
      else:
        departure_matching(author_dict, af_tokyo_dep, dep_match, paper_index)
        #print "dep_match: " + str(dep_match[paper_index])
    #    print "TARGET_TI: " + target['TI']
    #  print "==========="
      if dep_match[paper_index] == None:
        #print "論文執筆時の所属機関が不適切です"
        return
       #print "論文執筆時の所属機関が適切です"
  if af_tokyo[paper_index] and py_match[paper_index] and (dep_match[paper_index] == "MATCHED"):
    global record_num
    record_num = record_num + 1

    # contribution_weightを測定
    # 著者リストの配列を作る。
    paper_AU_list = target['AU'].split(';')
    # 著者リストを大文字にした配列を作る
    alist1 = map(lambda x:x.upper(), paper_AU_list)
    # alist2のために、大文字の配列をコピーする
    # これはalist2のためにしか使われない。
    sub_alist1 = map(lambda x:x.upper(), paper_AU_list)
    sub_alist1.pop(0)
    # alist2の２番目の配列（先頭を消去した配列）を作る
    alist2_second_factor = sub_alist1
    if alist2_second_factor is None:
      # alist2_second_factorが空の配列[]の時、cweightの処理が止まるから、固定値を返す。
      contribution_weight_calc_result = 1.0
    else:
      #print "contribution_weight not 1.0"
      alist2 = [[alist1[0]], alist2_second_factor]

      contribution_weight_calc_result = cw.cweight(cw.order_pattern(alist1), alist2, author_dict['faculty_name'].upper())

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
    tf.write('CW           =>'+str(contribution_weight_calc_result)+'\n')
    tf.write('FILE_NAME    =>'+str(text_name)+'\n')
    tf.write('PAPER_ID     =>'+str(paper_index)+'\n')
    tf.close()

    # wos_result.csvにその年の著者の論文出稿数の単純和と、インパクトファクターを書き込む
    # その後、wos_list.csvとwos_result.csvの内容を一致させる
    wtwr.write_to_wos_result(author_dict['id'], target['PY'], target['SO'], year_NA_flag[paper_index], dep_match[paper_index], contribution_weight_calc_result)
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
    if line.upper().find("UNIV TOKYO") >= 0:
      for x in inst_list:
        if x in listed_c1[i+1].upper():
          dep_list = listed_c1[i+1].upper().lstrip().lstrip()
        elif listed_c1[i+1].upper() == "FAC SCI":
          for sci_dep in fac_dep_list:
            if sci_dep in listed_c1[i+2].upper():
              dep_list = listed_c1[i+2].upper().lstrip().lstrip()
        #      print "FAC SCIがあった"
        elif listed_c1[i+1].upper() == "GRAD SCH SCI":
          for grad_dep in grad_dep_list:
            if grad_dep in listed_c1[i+2].upper():
              dep_list = listed_c1[i+2].upper().lstrip().lstrip()
        #      print "GRAD SCH SCIがあった"
        elif listed_c1[i+1].upper() == "COLL ARTS & SCI" or listed_c1[i+1].upper() == "COLL GEN EDUC":
          for liveral_dep in l_dep_list:
            if liveral_dep in listed_c1[i+2].upper():
              dep_list = listed_c1[i+2].upper().lstrip().lstrip()
              #print "Lの機関があった"
  return dep_list

# ブラックリストに入っている学部を除く   
def delete_dep(dep_list=[]):
  for i,line in enumerate(dep_list):
    for x in black_list:
      if x == dep_list:
        dep_list = []
  return dep_list

def C1_check(target_c1='', paper_index=0, af_tokyo={}, af_phys={}, af_tokyo_dep={}, tmp_dep={}):
  #print "TARGET_C1: " + target_c1
  #print target_c1
  if target_c1 == None or (not re.search('UNIV TOKYO', target_c1.upper())):
    #print "東京大学じゃありませんでした"
    C1_matching_flag[paper_index] = 0
    #print "だみでしたあああああああああああ"
    return
  else:
    af_tokyo[paper_index] = 1
    if re.search('UNIV TOKYO, DEPT PHYS', target_c1.upper()):
      #print "物理学科でした"
      af_phys[paper_index] = 1
      af_tokyo_dep[paper_index] = 'DEPT PHYS'
      C1_matching_flag[paper_index] = 1
    else:
      #print "物理学科じゃありません"
      tmp_dep[paper_index] = stock_dep(target_c1.upper())
      #print "TMP_DEPです~~~~~~~~~~~~~~~~~~"
      #print tmp_dep[paper_index]
      af_tokyo_dep[paper_index] = delete_dep(tmp_dep[paper_index])
      if af_tokyo_dep[paper_index] == []:
        C1_matching_flag[paper_index] = 0
        #print "物理学科だけどC1マッチしなかった…"
        return
      #print "AF_TOKYO_DEPです~~~~~~~~~~~~~~"
      #print af_tokyo_dep[paper_index]
      C1_matching_flag[paper_index] = 1
      af_phys[paper_index] = 0
        
def RP_check(target_rp='', target_c1='', paper_index=0, af_tokyo={}, af_phys={}, af_tokyo_dep={}, tmp_dep={}):
  # 著者の所属によるマッチング==========================
  #print "TARGET_RP: " + target_rp
  #print target_rp
  if not re.search('UNIV TOKYO', target_rp.upper()):
    af_tokyo[paper_index] = 0
    RP_matching_flag[paper_index] = 0
    C1_check(target_c1, paper_index, af_tokyo, af_phys, af_tokyo_dep, tmp_dep)
    #　RPCHECK2は大抵ここ 
    #print "だみでした"
    return
  else:
    #print "東京大学でした"
    af_tokyo[paper_index] = 1
    if re.search('UNIV TOKYO, DEPT PHYS', target_rp.upper()):
      #print "物理学科でした"
      af_phys[paper_index] = 1
      af_tokyo_dep[paper_index] = 'DEPT PHYS'
      RP_matching_flag[paper_index] = 1
    else:
      #print "物理学科じゃありません"
      # 適切な物理学研究機関かどうかを、学部・施設対応.xlsのリストから判別する
      tmp_dep[paper_index] = stock_dep(target_rp.upper())
      #print "TMP_DEPです2~~~~~~~~~~~~~~~~~~"
      #print tmp_dep[paper_index]
      af_tokyo_dep[paper_index] = delete_dep(tmp_dep[paper_index])

      #print "こことおってる1"
      if af_tokyo_dep[paper_index] == []:
        #print "こことおってだめぽ"
        RP_matching_flag[paper_index] = 0
        C1_check(target_c1, paper_index, af_tokyo, af_phys, af_tokyo_dep, tmp_dep)
        return
      #print "こことおってる2"
      #print "AF_TOKYO_DEPです2~~~~~~~~~~~~~~"
      #print af_tokyo_dep[paper_index]
      af_phys[paper_index] = 0
      RP_matching_flag[paper_index] = 1

def departure_matching(author_dict={}, af_tokyo_dep={}, dep_match={}, paper_index=0):
  # unit_strign は D,M,C,S,Pなどなど
  for unit_string in author_dict['dep']:
    #print "UNIT_STRING: " + unit_string
    for row in fdep_dict:
      if row[0] is unit_string:
        for unit_dep in row[1]:
          #print "UNIT_DEP: " + unit_dep
          if af_tokyo_dep[paper_index] == unit_dep:
            dep_match[paper_index] = "MATCHED"
          #  print "所属機関がマッチしました。"
            return
          else:
            dep_match[paper_index] = None
          #  print "所属機関がマッチしなかった"
