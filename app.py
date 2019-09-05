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


def search_index(id, type):
    search_body = {
        "query": {

            "bool": {

                "must": [{
                    "match": {"id": id},


                }],
                "filter": {"term": {"type": type}}
            }


        }

    }

    result = es.search(index="problems_test", body=search_body)["hits"]["hits"]
    return result


def search_problems(keyword):

    body = {
        "query": {


            "bool": {

                "must": [{
                    "match": {"title": keyword},


                }],
                "filter": {"term": {"type": "problem"}}
            }


        }

    }

    res = es.search(index="problems_test", body=body)

    return jsonify(res['hits']['hits'])


def search_solutions(keyword):
    body = {
        "query": {


            "bool": {

                "must": [{
                    "match": {"title": keyword},


                }],
                "filter": {"term": {"type": "solution"}}
            }


        }

    }

    res = es.search(index="problems_test", body=body)

    return jsonify(res['hits']['hits'])


@app.route('/', methods=['GET'])
def index():
    results = es.get(index='my_playlist', doc_type='song', id=6)
    # return "working"
    return jsonify(results['_source'])


@app.route('/insert_problem_index', methods=['POST'])
def insert_data():

    trigger_payload = request.json

    problem = trigger_payload["event"]["data"]["new"]

    if not problem["is_draft"]:

        problem["type"] = "problem"

        body = problem

        result = es.index(index='problems_test',
                          body=body)

        return jsonify(result)
    return "return for insert"


@app.route('/update_problem_index', methods=['POST'])
def index_problem():

    trigger_payload = request.json

    problem = trigger_payload["event"]["data"]["new"]
    search_result = search_index(problem["id"], "problem")
    body = problem
    problem["type"] = "problem"

    if not problem["is_draft"]:
        if search_result and len(search_result) and search_result[0]["_id"]:
            id = search_result[0]["_id"]

            result = es.index(index='problems_test', id=id,
                              body=body)

    else:
        result = es.index(index='problems_test',
                          body=body)

    return jsonify(result)


@app.route('/solution_index', methods=['POST'])
def index_solution():

    trigger_payload = request.json

    solution = trigger_payload["event"]["data"]["new"]
    search_result = search_index(solution["id"], "solution")
    body = solution
    solution["type"] = "solution"

    if not solution["is_draft"]:
        if search_result and len(search_result) and search_result[0]["_id"]:
            id = search_result[0]["_id"]

            result = es.index(index='problems_test', id=id,
                              body=body)

    else:
        result = es.index(index='problems_test',
                          body=body)

    return jsonify(result)


@app.route('/user_index', methods=['POST'])
def index_user():

    trigger_payload = request.json

    user = trigger_payload["event"]["data"]["new"]
    search_result = search_index(user["id"], "user")
    body = user
    user["type"] = "user"

    if search_result and len(search_result) and search_result[0]["_id"]:
        id = search_result[0]["_id"]

        result = es.index(index='problems_test', id=id,
                          body=body)

    else:
        result = es.index(index='problems_test',
                          body=body)

    return jsonify(result)


@app.route('/global_search', methods=['POST'])
def search():
    print("request===", request.json)
    req = request.json
    keyword = req["keyword"]

    body = {
        "query": {


            "bool": {

                "must": [{
                    "match": {"name": keyword},


                }],
                "filter": {"term": {"type": "user"}}
            }


        }

    }

    user_results = es.search(index="problems_test", body=body)['hits']['hits']
    solution_results = search_solutions(keyword)
    problem_results = search_problems(keyword)

    results = {
        "users": user_results,
        "problems": problem_results,
        "solutions": solution_results
    }

    results = jsonify(results)
    results.status_code = 200

    return jsonify(results)


if __name__ == "__main__":
    # app.run(debug=True)
    serve(app, listen='*:{}'.format(str(PORT)))
