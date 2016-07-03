from flask import Flask, request, jsonify
import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh import highlight

app = Flask(__name__)

ix = index.open_dir("indexdir")
qp = QueryParser("content", schema=ix.schema)
searcher = ix.searcher()


class NullFormatter(highlight.Formatter):
    def format_token(self, text, token, replace=False):
        tokentext = highlight.get_text(text, token, replace)
        return tokentext


@app.route("/search")
def search():
    keyword = request.args.get('keyword', '')
    q = qp.parse(keyword)
    results = searcher.search(q, limit=None, terms=True)
    results.formatter = NullFormatter()

    rt = []
    for hit in results:
        rt.append({
            "title": hit.get("title", "untitle"),
            "highlights": hit.highlights("content"),
            "url": "https://g0v.hackpad.com{}".format(hit.get("path", "")),
        })

    return jsonify(rt)


if __name__ == "__main__":
    app.run()
