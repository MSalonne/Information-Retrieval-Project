import json, os
from math import log, sqrt
from numpy import dot
from numpy.linalg import norm

class Index:
    def __init__(self):
        json_file_name = os.path.join(".", "index.json")
        self.index = dict(json.load(open(json_file_name))) 
        json_file_name = os.path.join(".", "bookkeeping.json")
        self.url_map = dict(json.load(open(json_file_name)))
        self.query = ''
    
    def retrieve_results(self):
        results = set()
        for i in self.query:
            try:
                for doc in self.index[i].keys():
                    results.add(doc)
            except KeyError:
                continue
        return results
    
    def rank_results(self):
        if len(self.query) == 1:
            try:
                return {kv[0]:self.url_map[kv[0]] for kv in sorted(self.index[self.query[0]].items(),
                    key=lambda kv:kv[1], 
                    reverse=True)}
            except KeyError:
                return {}
        else:
            scores, query_idfs= {}, {}
            docs = self.retrieve_results()
            #calculating tf-idfs of query terms
            for i in self.query: 
                try:
                    query_idfs[i] = (1 + log(self.query.count(i), 10))*(log(len(self.url_map)/len(self.index[i].keys()), 10))
                except KeyError:
                    query_idfs[i] = 0

            #normalization of docs tfidfs
            for doc in docs:
                norml_tfidf = {}
                score = 0
                for i in self.query:
                    try:
                        norml_tfidf[i] = self.index[i][doc]
                    except KeyError:
                        norml_tfidf[i] = 0

                score = dot(list(query_idfs.values()), list(norml_tfidf.values()))/norm(list(query_idfs.values()))*norm(list(norml_tfidf.values()))
                scores[doc] = score

            return {kv[0]:self.url_map[kv[0]] for kv in sorted(scores.items(), key=lambda kv:kv[1], reverse = True) if kv[1] >= 0.4}