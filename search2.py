# coding=utf-8
import os
import json
import whoosh.index as index
from whoosh.qparser import QueryParser

ix = index.open_dir("indexdir2")
qp = QueryParser("readme", schema=ix.schema)

# 创建一个检索器
searcher = ix.searcher()

i = 0

while i == 0:
    user_input = input(
        "Some input please: ")  # or `input("Some...` in python 3
    q = qp.parse(user_input)
    results = searcher.search(q, limit=None)
    print ("result count = " + str(len(results)))
    for res in results:
        ff = res.fields()
        jsondoc = json.dumps(ff, ensure_ascii=False)

        # jsondoc.score = res.score
        #print(res)
        #print(res['f'])
        if 'repo_name' in res:
            print(res['repo_name'])
        else:
            print('untitled')
        print(res.score)

    # print(res.fields())
    # print(jsondoc)  # 打印出检索出的文档全部内容
    # # 检索出来的第一个结果，数据格式为dict{'title':.., 'content':...}
    # firstdoc = results[0].fields()

    # # python2中，需要使用json来打印包含unicode的dict内容
    # jsondoc = json.dumps(firstdoc, ensure_ascii=False)

    # print(jsondoc)  # 打印出检索出的文档全部内容
    # print(results[0].highlights("title"))  # 高亮标题中的检索词
    # print(results[0].score)  # bm25分数
