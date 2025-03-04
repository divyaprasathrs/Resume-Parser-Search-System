
from flask import Flask, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)


es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "Qq1E-kzDt8d2OAlpZvOF"), verify_certs=False)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Resume API! Use /resume/<id> to fetch a resume."})

@app.route("/resume/<id>", methods=["GET"])
def get_resume(id):
    try:
        response = es.get(index="task5", id=id)
        return jsonify(response["_source"])
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/resumes", methods=["GET"])
def list_resumes():
    query = {"query": {"match_all": {}}}
    response = es.search(index="task5", body=query, size=10) 
    resumes = [hit["_source"] for hit in response["hits"]["hits"]]
    return jsonify(resumes)

if __name__ == "__main__":
    app.run(debug=True)

