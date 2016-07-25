# coding=utf-8
import os,sys,re,time,json
from os import walk

from whoosh.index import create_in
from whoosh.fields import *
import whoosh.index as index
from whoosh.filedb.filestore import FileStorage
from jieba.analyse import ChineseAnalyzer

import argparse


# -------- Argument Parser Setting --------
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', default='', nargs='+' ,help='index output directory')

# -------- Retrieve Arg Options --------
arg = parser.parse_args()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_file = BASE_DIR + '/data.json'


sys.setrecursionlimit(200000)

# read old data and last update time
try:
    with open(json_file) as data_file:
        old_info = json.load(data_file)
        last_update = old_info['last_update']
except:
    old_info = {}
    old_info['repos'] = {}
    last_update = 0

# update data.json

os.system('python3 ' + BASE_DIR + '/get-g0v-repos.py')

with open(json_file) as data_file:
    new_info = json.load(data_file)

# update index
to_update = {}
for k, v in new_info['repos'].items():
    if k not in old_info['repos']:
        to_update[k] = new_info['repos'][k]
    elif v['updated_at'] > old_info['repos'][k]['updated_at']:
        to_update[k] = new_info['repos'][k]


#print("總共 " + str(len(data)) + " 個 ")
print("上次建立時間：" + time.ctime(float(last_update)))
print("需要更新數量：" + str(len(to_update)))
print("開始建立分詞索引")
print("===================================")

# 使用结巴中文分词
analyzer = ChineseAnalyzer()

# 创建schema, stored为True表示能够被检索
#schema = Schema(source_type=TEXT(stored=True),
#                repo_owner=TEXT(stored=True),
#                repo_name=TEXT(stored=True, analyzer=analyzer),
#                repo_url=ID(stored=True, unique=True),
#                created_at=TEXT(stored=True),
#                updated_at=TEXT(stored=True),
#                repo_html_url=TEXT(stored=True),
#                readme=TEXT(stored=True, analyzer=analyzer),
#                readme_url=TEXT(stored=True))

schema = Schema(guid=ID(stored=True),
                source_type=TEXT(stored=True),
                title=TEXT(stored=True),
                content=TEXT(stored=True, analyzer=analyzer),
                created_at=TEXT(stored=True),
                updated_at=TEXT(stored=True),
                repository=TEXT(stored=True),
                category=TEXT(stored=True,analyzer=analyzer),
                owner=TEXT(stored=True))

# 按照schema定义信息，增加需要建立索引的文档
# 注意：字符串格式需要为unicode格式

# 存储schema信息至'indexdir'目录下
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
indexdir = BASE_DIR + '/indexdir/'

if arg.output[0] != '':
    indexdir = arg.output[0]

if not os.path.exists(indexdir):
    os.mkdir(indexdir)
    storage = FileStorage(indexdir)
    ix = create_in(indexdir, schema)
else:
    ix = index.open_dir(indexdir)
    # ix = create_in(indexdir, schema)
    print("open")

# write index
writer = ix.writer()

for k, v in to_update.items():

    writer.update_document(guid="github_%s" % v['repo_url'],
                        source_type='g0v-repos',
                        title=v['repo_name'],
                        content=re.sub('[\s+]', '', v['readme_raw']),
                        created_at=v['created_at'],
                        updated_at=v['updated_at'],
                        repository=v['repo_url'],
                        #category=
                        #repo_html_url=v['repo_html_url'],
                        #readme_url=v['readme_url']
                        owner=v['repo_owner'])


    print( v['repo_name'] + " | " + v['updated_at'])


writer.commit(merge=True)


print("done")
