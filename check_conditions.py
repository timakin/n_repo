# coding:utf-8
import re
import os
import import_author_list as im
import write_to_wos_result as wtwr
from collections import OrderedDict

dict_for_author = {}
imported_dict = im.return_author_list(dict_for_author)
full_match       = {}
af_tokyo         = {}
af_phys         = {}
af_tokyo_dep     = {}
py_match         = {}
dep_list        = {}
unique_dep_list  =  []
record_num       = 0
tmp_dep = {}

def return_conditions(target={}, author_dict={}, text_name='', paper_index=0):
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

    if target['C1'] == None or ((not re.search('UNIV TOKYO', target['C1'].upper())) and (not re.search('UNIV TOKYO', str(target['RP']).upper()))):
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
      if author_dict['start_year'] is '':
        author_dict['start_year'] = author_dict['end_year']
      elif '?' in author_dict['start_year']:
        author_dict['start_year']=author_dict['start_year'].replace("?", "")
      elif '?' in author_dict['end_year']:
        author_dict['end_year']=author_dict['end_year'].replace("?", "")
      time_span = range(int(author_dict['start_year']), int(author_dict['end_year']))
      if int(target['PY']) not in time_span:
        print "所属期間内に論文が出ていません"
        return
      else:
        print "所属期間内に論文がでました"
        py_match[paper_index] = 1

  if af_tokyo[paper_index] and py_match[paper_index]:
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



# 以下が所属学科を配列として取得する処理
# 1.「,」でsplit。研究機関と所属学科ごとに改行する。
# 2.「UNIV TOKYO」の後の行をdep_list[author_dict['id']]に入れる

inst_list = ["DEPT",
             "INST",
             "FAC",
             "DIV",
             "COLL",
             "GRAD",
             "CTR"]
black_list = ["INST SPACE & AERONAUT SCI",
              "INST SPACE & ASTRON SCI",
              "ADV SCI & TECHNOL RES CTR",
              "ADV SCI TECHNOL RES CTR",
              "CTR ISOTOPE",
              "CTR RADIOISOTOPE",
              "DEPT ASTRON",
              "DEPT BASIC SCI",
              "INST ASTRO",
              "INST ASTRON",
              "INST PHYS",
              "INST PHYS & ASTRON",
              "INST PHYS & MATH",
              "INST PHYS & MATH UNIV",
              "INST PHYS & MATH UNIVERSE",
              "INST PHYS & MATH UNIVERSE IPMU",
              "NUCL SCI & TECHNOL RES CTR",
              "NUCL SCI & TECHNOL RES INST",
              "BIOSCI RES INST",
              "CTR COMP",
              "CTR CRYOGEN",
              "CTR CYTOGENET",
              "CTR ENVIRONM SCI",
              "DEPT ADV MAT",
              "DEPT ADV MAT SCI",
              "DEPT AGR CHEM",
              "DEPT APPL BIOL CHEM",
              "DEPT APPL CHEM",
              "DEPT APPL MATH",
              "DEPT APPL PHYS",
              "DEPT APPL SCI",
              "DEPT BIOCHEM & BIOTECHNOL",
              "DEPT BIOL",
              "DEPT BIOPHYS & LIFE SCI",
              "DEPT BIOTECHNOL",
              "DEPT BUNKYO KU",
              "DEPT CHEM",
              "DEPT CHEM ENGN",
              "DEPT COMP SCI",
              "DEPT EARTH & PLANETARY PHYS",
              "DEPT EARTH & PLANETARY SCI",
              "DEPT EARTH SCI & ASTRON",
              "DEPT ELECT & INFORMAT",
              "DEPT ELECT ENGN",
              "DEPT GEOPHYS",
              "DEPT IND & ENGN CHEM",
              "DEPT IND CHEM",
              "DEPT IND MANAGEMENT",
              "DEPT INFORMAT SCI",
              "DEPT INTERNAL MED 3",
              "DEPT LIFE SCI",
              "DEPT MAT ENGN",
              "DEPT MAT SCI & TECHNOL",
              "DEPT MATH",
              "DEPT MATH SCI",
              "DEPT MECH ENGN",
              "DEPT MED & PHYS THERAPY",
              "DEPT MED SCI",
              "DEPT PHARMACEUT SCI",
              "DEPT PHYSIOL CHEM & NUTR",
              "DEPT PURE & APPL SCI",
              "DEPT QUANTUM ENGN & SYST SCI",
              "DEPT SYNTHET CHEM",
              "DEPT VET PHYSIOL",
              "DIV LASER PHYS",
              "DIV MED",
              "EARTHQUAKE RES INST",
              "ENGN RES INST",
              "FAC AGR",
              "FAC CHEM",
              "FAC ENGN",
              "FAC IND SCI & TECHNOL",
              "FAC MED",
              "FAC PHARM SCI",
              "FAC PHARMACEUT SCI",
              "FAC SCI",
              "FAC SCI & TECHNOL",
              "FAC SURG",
              "FAC TECHNOL",
              "GRAD SCH ENGN",
              "GRAD SCH FRONTIER SCI",
              "GRAD SCH MED",
              "INST APPL MICROBIOL",
              "INST COLLOID & INTERFACE CHEM",
              "INST COLLOID & INTERFACE SCI",
              "INST ENGN INNOVAT",
              "INST ENGN RES",
              "INST GEN INFIRM",
              "INST GEOL",
              "INST GEOPHYS",
              "INST IND SCI",
              "INST MATH",
              "INST MED SCI",
              "INST MINERAL",
              "INST MOLEC & CELLULAR BIOSCI",
              "INST NANO QUANTUM INFORMAT ELECT",
              "INST NANO QUANTUM INFORMAT ELECTRON",
              "INST NUCL SAFETY",
              "OCEAN RES INST",
              "QPEC & DEPT APPL PHYS",
              "RES CTR ADV SCI & TECHNOL",
              "SCI & TECHNOL RES INST",
              "SCI RES INST",
              "TECHNOL RES INST"]

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
        
