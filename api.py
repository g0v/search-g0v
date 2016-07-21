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

    return jsonify(rt)


if __name__ == "__main__":
    app.run()
