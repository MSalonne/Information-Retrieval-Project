import json, os, urllib.request, re
from bs4 import BeautifulSoup
from inverted_index import Inverted_index
from collections import defaultdict

def process_file(line):
    word_bag = defaultdict(int)
    regex = re.compile('[^a-zA-Z0-9]')               # alphanumeric characters are to be tokenized
    lines = regex.sub(' ', line.lower())
    lines = lines.split()   
    for word in lines:                              # takes a list of tokens and adds them into word_bag with
        word_bag[word] += 1                          # the respective frequencies
    return word_bag

def get_map(fil):
    json_file_name = os.path.join(".", fil)
    urls_json = json.load(open(json_file_name))
    return dict(urls_json)

def create_invidx():
    invidx = Inverted_index()
    addrs = get_map("bookkeeping.json")
    invidx.totalDocs = len(addrs)
    for local_file in addrs.keys():
        dir = local_file.split("/")
        file = dir[1]
        html_ =  open(os.path.join(".","WEBPAGES_RAW",dir[0],file), encoding='utf8')
        soup = BeautifulSoup(html_, 'html.parser')
        soup_text = soup.findAll(text=True)
        clean_soup = ""
        for text in soup_text:
            if text.parent.name not in ['[document]', 'script', 'style', 'meta', 'head']:
                if text.split() != []:
                    clean_soup = clean_soup + ' ' + ' '.join(text.split())
                
        bag  = process_file(clean_soup)
        invidx.add(bag, local_file)
    
    invidx.tf_idf()
    invidx.save_to_json()

if __name__ == '__main__':
    create_invidx()