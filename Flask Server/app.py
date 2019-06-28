from flask import Flask, jsonify, request, make_response
from elasticsearch import Elasticsearch

import os
import json
import numpy as np
import ast
import re
from numpy import linalg as LA

from query_preprocessing import expand_query

app = Flask(__name__)
es = Elasticsearch('http://localhost:9200/')

@app.route("/")
def index():
    return expand_query("securit")
    # return "hello"


@app.route("/info")
def es_info():
    result = es.info()
    return jsonify(result)


def cosine_similarity(a, b):
    if (LA.norm(a) and LA.norm(b)):
        return (np.dot(a, b) / (LA.norm(a) * LA.norm(b)))
    return 0


def get_video_and_time(query, json_list):
    trans_md = []
    corpus_index = {}
    doc_matrix = []
    video_folder_names = []
    for video_folder in json_list:
        video_folder_names.append(video_folder[0]["video_name"])
        trans_md.append([])
        doc_vector = [0] * len(corpus_index)

        for line_dict in video_folder:
            del line_dict["video_name"]
            del line_dict["row_id"]
            trans_md[len(trans_md) - 1].append(line_dict)
            for word in re.findall(r"[\w']+", line_dict["row_content"].lower()):
                ##Assuming we don't deal with integer overflow for corpus size:p
                corpus_index[word] = min(corpus_index.get(word, len(corpus_index) + 1), len(corpus_index))
                if (len(doc_vector) < len(corpus_index)):
                    doc_vector.append(1)
                    for index in range(len(doc_matrix)):
                        doc_matrix[index].append(0)
                else:
                    doc_vector[corpus_index[word]] += 1

        doc_vector = list(np.array(doc_vector) / np.sum(doc_vector))
        doc_matrix.append(doc_vector)
    doc_matrix = np.array(doc_matrix)

    corpus_idf = []
    for col in range(len(corpus_index)):
        df = np.count_nonzero(doc_matrix[:, col])
        idf = np.log(doc_matrix.shape[0] / df + 1)
        corpus_idf.append(idf)
        doc_matrix[:, col] *= idf

    query_vector = np.zeros(len(corpus_index))
    for word in re.findall(r"[\w']+", query.lower()):
        index = corpus_index.get(word, None)
        if index:
            query_vector[index] += 1
    query_vector /= max(np.sum(query_vector), 1)
    query_vector = np.multiply(query_vector, corpus_idf)

    max_similarity = 0

    results = []
    for index in range(doc_matrix.shape[0]):
        similarity = cosine_similarity(query_vector, doc_matrix[index])
        results.append((-similarity, index))

    results = sorted(results)[:min(10, len(results))]

    dict_results = {}
    order = 1
    for _, matching_video_id in results:
        corpus_index = {}
        doc_matrix = []
        for line_dict in trans_md[matching_video_id]:
            doc_vector = [0] * len(corpus_index)
            for word in re.findall(r"[\w']+", line_dict["row_content"].lower()):
                ##Assuming we don't deal with integer overflow for corpus size:p
                corpus_index[word] = min(corpus_index.get(word, len(corpus_index) + 1), len(corpus_index))
                if (len(doc_vector) < len(corpus_index)):
                    doc_vector.append(1)
                    for index in range(len(doc_matrix)):
                        doc_matrix[index].append(0)
                else:
                    doc_vector[corpus_index[word]] += 1
            doc_vector = list(np.array(doc_vector) / np.sum(doc_vector))
            doc_matrix.append(doc_vector)
        doc_matrix = np.array(doc_matrix)

        corpus_idf = []
        for col in range(len(corpus_index)):
            df = np.count_nonzero(doc_matrix[:, col])
            idf = np.log(doc_matrix.shape[0] / df + 1)
            corpus_idf.append(idf)
            doc_matrix[:, col] *= idf

        query_vector = np.zeros(len(corpus_index))
        for word in re.findall(r"[\w']+", query.lower()):
            index = corpus_index.get(word, None)
            if index:
                query_vector[index] += 1
        query_vector /= max(np.sum(query_vector), 1)
        query_vector = np.multiply(query_vector, corpus_idf)

        results = []
        for index in range(doc_matrix.shape[0]):
            similarity = cosine_similarity(query_vector, doc_matrix[index])
            results.append((-similarity, index))

        results = sorted(results)[:min(5, len(results))]
        result_md = []
        for _, result in results:
            result_md.append(trans_md[matching_video_id][result])

        dict_results[str(order)] = {"video_name": video_folder_names[matching_video_id], "time_list": result_md}
        order += 1

    return dict_results


@app.route("/search", methods=['GET', 'POST'])
def search():
    keyword = request.form['keyword']
    keyword = expand_query(keyword)
    print(keyword)
    # body = {
    #     "query": {
    #         "bool": {
    #             "must": {
    #                 "multi-match": {
    #                     "query": keyword,
    #                     "fuzziness": "2",
    #                     "fields": ["row_content"],
    #                     "minimum_should_match": "80%",
    #                     "type": "most_fields"
    #                 }
    #             }
    #         }
    #     },
    #     "highlight": { "fields": { "row_content": { "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] } } }
    # }

    body = {
        "query": {
            "match": {
                "row_content": keyword
            }
        },
        "highlight": { "fields": { "row_content": { "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] } } }
    }
    resp = es.search(index="transcript", doc_type="_doc", body=body)

    resp_for_tf = resp['hits']['hits']
    print(resp_for_tf)
    resp_group_by_name = {}
    for resp_item in resp_for_tf:
        group_items = resp_group_by_name.get(resp_item['_source']['video_name'], [])
        resp_source = resp_item['_source']
        resp_source['highlight'] = resp_item['highlight']['row_content'][0]
        group_items.append(resp_source)
        resp_group_by_name[resp_item['_source']['video_name']] = group_items

    resp_values = list(resp_group_by_name.values())
    sorted_result = get_video_and_time(keyword, resp_values)
    # print(sorted_result)

    resp = make_response(jsonify(sorted_result), 200)
    resp.headers.add("Access-Control-Allow-Origin", "*")
    resp.headers.add("Access-Control-Allow-Headers", "*")
    resp.headers.add("Access-Control-Allow-Methods", "*")

    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6789, debug=True)
