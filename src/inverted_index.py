import json
import math
from collections import defaultdict
from nltk.corpus import stopwords

class Inverted_index:
    def __init__(self):
        self.stopwords = stopwords.words("english")
        self.totalDocs = 0
        self.db = defaultdict(dict)

    def add(self, bag, local_file):
        for term in bag.keys():
            if term not in self.stopwords:
                self.db[term][local_file] = bag[term]
    
    def tf_idf(self):
        for term in self.db.keys():
            for local_file in self.db[term].keys():
                if self.db[term][local_file] != 0.0:
                    self.db[term][local_file] = (1 + math.log(self.db[term][local_file], 10))*(math.log(self.totalDocs/len(self.db[term].keys()), 10))
                    
    def save_to_json(self):
        with open('index.json', 'w') as json_file:
            json.dump(self.db, json_file)