from flask import Flask, jsonify, request, make_response
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('http://10.2.214.209:9200/')

@app.route("/")
def index():
    return "hello"

@app.route("/info")
def es_info():
    result = es.info()
    return jsonify(result)

@app.route("/search", methods=['GET', 'POST'])
def search():
    keyword = request.form['keyword']
    print(keyword)
    body = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": keyword,
                        "fuzziness": "1",
                        "fields": ["row_content"],
                        "minimum_should_match": "80%",
                        "type": "most_fields"
                    }
                }
            }
        },
        "highlight": { "fields": { "row_content": { "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] } } }
    }

    resp = es.search(index="transcript", doc_type="_doc", body=body)
    resp = jsonify(resp['hits']['hits'])

    resp = make_response(resp, 200)
    resp.headers.add("Access-Control-Allow-Origin", "*")
    resp.headers.add("Access-Control-Allow-Headers", "*")
    resp.headers.add("Access-Control-Allow-Methods", "*")

    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6789, debug=True)
