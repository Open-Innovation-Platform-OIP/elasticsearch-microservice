import os
from flask import Flask, request, jsonify
import json
from waitress import serve
from elasticsearch import Elasticsearch, RequestsHttpConnection
# from ssl import create_default_context

# context = create_default_context(cafile="path/to/cafile.pem")


es = Elasticsearch([{'host': "157.245.111.179"}], port=9200, connection_class=RequestsHttpConnection,
                   http_auth=('admin', 'admin'), use_ssl=True, verify_certs=False)
es.info()


app = Flask(__name__)

PORT = 8080


@app.route('/', methods=['GET'])
def index():
    results = es.get(index='my_playlist', doc_type='song', id=6)
    # return "working"
    return jsonify(results['_source'])


@app.route('/insert_problem_index', methods=['POST'])
def insert_data():
    # slug = request.form['slug']
    # title = request.form['title']
    # content = request.form['content']

    trigger_payload = request.json

    problem_id = trigger_payload["event"]["data"]["new"]["id"]

    problem = trigger_payload["event"]["data"]["new"]

    body = problem

    result = es.index(index='problems', doc_type='problem',
                      id=problem_id, body=body)

    return jsonify(result)


@app.route('/search', methods=['POST'])
def search():
    print("request===", request)
    keyword = request.json['keyword']

    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["description", "title"]
            }
        }
    }

    res = es.search(index="problems", body=body)

    return jsonify(res['hits']['hits'])


if __name__ == "__main__":
    # app.run(debug=True)
    serve(app, listen='*:{}'.format(str(PORT)))
