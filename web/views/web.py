from flask import Flask, request, jsonify, Response, Blueprint,render_template
import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh import highlight


mod = Blueprint('web',__name__)

ix = index.open_dir("indexdir")
qp = QueryParser("content", schema=ix.schema)
searcher = ix.searcher()


class NullFormatter(highlight.Formatter):
    def format_token(self, text, token, replace=False):
        tokentext = highlight.get_text(text, token, replace)
        return tokentext


@mod.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('search.html')

    keyword = request.form['keyword']


    page = request.args.get('page', "1")
    q = qp.parse(keyword)
    results = searcher.search_page(q, int(page), terms=True)
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

    #resp = jsonify(rt)
    #resp.headers['Access-Control-Allow-Origin'] = '*'
    #resp.headers['Content-Type'] = 'text/json; charset=utf-8'
    #return resp

    return render_template('search.html',keyword=keyword,results=rt)

    #resp = jsonify(rt)
    #resp.headers['Access-Control-Allow-Origin'] = '*'
    #resp.headers['Content-Type'] = 'text/json; charset=utf-8'
    #return resp
