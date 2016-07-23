from flask import Flask, request, jsonify, Response, Blueprint
import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh import highlight

mod = Blueprint('api', __name__, url_prefix='/api')

ix = index.open_dir("indexdir")
qp = QueryParser("content", schema=ix.schema)
searcher = ix.searcher()


class NullFormatter(highlight.Formatter):
    def format_token(self, text, token, replace=False):
        tokentext = highlight.get_text(text, token, replace)
        return tokentext


@mod.route("/search")
def search():
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', "1")
    q = qp.parse(keyword)
    results = searcher.search_page(q, int(page), terms=True)
    results.formatter = NullFormatter()

    rt = []
    for hit in results:
        obj = {
            "title": hit.get("title", "untitle"),
            "highlights": hit.highlights("content"),
            "url": hit.get("repository",""),
        }

        rt.append(obj)

    resp = jsonify(rt)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'text/json; charset=utf-8'
    return resp
