# coding=utf-8
import os
import json
import whoosh.index as index
from whoosh.qparser import QueryParser

ix = index.open_dir("indexdir")
qp = QueryParser("content", schema=ix.schema)

# 创建一个检索器
searcher = ix.searcher()

i = 0

while i == 0:
    user_input = input(
        "Some input please: ")  # or `input("Some...` in python 3
    q = qp.parse(user_input)
    results = searcher.search(q, limit=None)
    print('result count: ' + str(len(results)))
    for res in results:
        ff = res.fields()
        jsondoc = json.dumps(ff, ensure_ascii=False)

        # jsondoc.score = res.score
        print(res)
        if 'title' in res:
            print(res['title'])
        else:
            print('untitled')
        print(res.score)
