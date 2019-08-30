import os
from flask import Flask, request, jsonify
import json
from waitress import serve
from elasticsearch import Elasticsearch
# from ssl import create_default_context

# context = create_default_context(cafile="path/to/cafile.pem")


es = Elasticsearch('host': "https://157.245.111.179:9200",
                   http_auth=('admin', 'admin'), verify_certs=False)
es.info()


app = Flask(__name__)

PORT = 8080


@app.route('/', methods=['GET'])
def index():
    results = es.get(index='contents', doc_type='title', id='my-new-slug')
    return jsonify(results['_source'])


@app.route('/insert_data', methods=['POST'])
def insert_data():
    slug = request.form['slug']
    title = request.form['title']
    content = request.form['content']

    body = {
        'slug': slug,
        'title': title,
        'content': content,

    }

    result = es.index(index='contents', doc_type='title', id=slug, body=body)

    return jsonify(result)


@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']

    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["content", "title"]
            }
        }
    }

    res = es.search(index="contents", doc_type="title", body=body)

    return jsonify(res['hits']['hits'])


if __name__ == "__main__":
    # app.run(debug=True)
    serve(app, listen='*:{}'.format(str(PORT)))
