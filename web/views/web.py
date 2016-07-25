from flask import Flask, request, jsonify, Response, Blueprint,render_template
import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh import highlight
import json, time

mod = Blueprint('web',__name__)

ix = index.open_dir("indexdir")
qp = QueryParser("content", schema=ix.schema)
searcher = ix.searcher()


class NullFormatter(highlight.Formatter):
    def format_token(self, text, token, replace=False):
        tokentext = highlight.get_text(text, token, replace)
        return tokentext

def search(keyword,page=1):

    if keyword == '':
        return render_template('search.html')

    q = qp.parse(keyword)
    t0 = time.time()
    results = searcher.search_page(q, int(page), terms=True)
    t1 = time.time()
    results.formatter = NullFormatter()

    rt = []
    for hit in results:
        obj = {
            "title": hit.get("title", "untitle"),
            "source": hit.get("source_type","unknown"),
            "highlights": hit.highlights("content"),
            "url": hit.get("repository",""),
        }
        rt.append(obj)

    # build pagination
    pages = []
    for index in range(1,results.pagecount):
        obj = {
            "active": index==results.pagenum,
            "title": index,
            "url": "?keyword=%s&page=%s" % (keyword, index)
        }
        pages.append(obj)

    search = {
        "time": t1-t0,
        "keyword": keyword,
        "count": results.total,
        "pagenum": results.pagenum,
        "pagecount": results.pagecount,
        "pages": pages,
        "results": rt
    }
    return render_template('search.html',keyword=keyword,search=search)


@mod.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        keyword = request.args.get('keyword','')
        page = request.args.get('page', "1")
        return search(keyword,page)

    keyword = request.form['keyword']
    return search(keyword)
