from flask import Flask, request, jsonify
import json
from waitress import serve

import os


app = Flask(__name__)

PORT = 8080


@app.route("/")
def entry():

    print("testing")
    return "working"


if __name__ == "__main__":
    # app.run(debug=True)
    serve(app, listen='*:{}'.format(str(PORT)))
