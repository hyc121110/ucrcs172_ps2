# note: the calculation of idf is 1 + log(N)/(n_k+1) instead of 1 + log(N)/(n_k)

import create_index
import os
import string
import sys
import math
from collections import defaultdict

from numpy import zeros
from numpy import dot
from numpy.linalg import norm

# posting index
posting_index = create_index.posting_index
# document index
document_index = create_index.document_index


# function to calculate cosine similarity between document and query
def cosineSim(d1, d2):
  res = float(dot(d1,d2) / (norm(d1) * norm(d2)))
  return res


# function to calculate tfidf score of words in posting_index
def tfidf_doc(query):
  # calculate tf-idf for each document
  tfidf_list = list()
  posting_list = posting_index[query][1]
  # iterate every occurence in each document and store the respective tfidf
  for i in range(len(posting_list)):
    # get the doc and freq
    doc = posting_list[i][0]
    freq = posting_list[i][1]
    # calculate tf
    tf = freq / document_index[doc]
    # calculate idf
    N = len(document_index)
    n_k = posting_index[query][0]
    idf = 1 + math.log(N)/(n_k+1)
    # calculate tf-idf
    tfidf = tf * idf
    tfidf_list.append((doc, tfidf))
  return tfidf_list


# function to calculate tfidf score of words in query
def tfidf_query(word, query):
  cnt = defaultdict(int)
  for q in query:
    cnt[q] += 1
  # calculate tf
  tf = cnt[word] / len(query)
  # calculate idf
  N = len(document_index)
  n_k = posting_index[word][0]
  idf = 1 + math.log(N)/(n_k+1)
  # calculate tf-idf
  tfidf = tf * idf
  return tfidf

# main
user_path = os.getcwd() # get current path

path = sys.argv[1] # directory
f = sys.argv[2] # query list
result = sys.argv[3] # write to result

# delete existing result file if exists
if os.path.exists(user_path + "\\" + result):
  os.remove(result)

full_path = user_path + "\\" + path + "\\" + f

# array of vectors for documents
docs_vec = list()
# dictonary for mapping document number
doc_num_dict1 = dict()
# dictionary for mapping reverse documenr number
doc_num_dict2 = dict()
# create vector for each doc
for i in range(len(document_index)):
  docs_vec.append([0] * len(posting_index))
  # map doc num to index and vice versa
  doc_num_dict1[list(document_index)[i]] = i
  doc_num_dict2[i] = list(document_index)[i]

# process queries
queries = create_index.processQueries(full_path)

# dictionary for identifying word
key_dict = dict()
# map key in posting index to numbers
idx = 0
for key in posting_index:
  key_dict[key] = idx
  idx += 1
 
# process each word in posting_index, calculate the tfidf and fill in the vector of respective document
for key in posting_index:
  tfidf_list = tfidf_doc(key)
  idx = key_dict[key]
  for tup in tfidf_list:
    # tup[0]: document id
    # doc_num_dict1[tup[0]]: document number
    # docs_vec[doc_num_dict1[tup[0]]][idx]: tfidf score of key at document
    docs_vec[doc_num_dict1[tup[0]]][idx] = tup[1]

# compare document vector and query vector
with open('stoplist.txt') as f1:
  stop_words = f1.read()
  for query in queries:
    # create new query vector
    v = [0] * len(posting_index)
    # check if query is a number
    first = True
    # remove all stopwords, remove punctuation, lowercase and stem the word first
    new_query = list()
    # check if number is a query number
    first = True
    # get rid of redundant words from query
    for q in query:
      if any(str.isdigit(c) for c in q) and first:
        # query number
        q_num = q.rstrip('.') # remove the period
        first = False
      elif q not in stop_words and not any(str.isdigit(c) for c in q):
        # word preprocessing
        q = create_index.remove_punctuation_lowercase(q)
        q = create_index.stemming(q)
        new_query.append(q)
    # process new query
    for q in new_query:
      if q in key_dict:
        tfidf = tfidf_query(q, new_query)
        idx = key_dict[q]
        lst = posting_index[q][1]
        for tup in lst:
          # tup[0]: document id
          v[idx] = tfidf
    # calculate cosine sim score for each doc
    scores = list()
    for idx, vec in enumerate(docs_vec):
      score = cosineSim(v, vec)
      scores.append((score, doc_num_dict2[idx]))
    scores = sorted(scores, reverse=True)

    # only top 20 results are needed
    max_scores = 20
    cnt = 0
    for score, doc_no in scores:
      if score > 0.0 and cnt < max_scores:
        # write result to file
        # <query number> Q0 <docno> <rank> <score> Exp
        cnt += 1
        with open("result_vsm.txt", "a") as myfile:
          myfile.write(q_num + " Q0 " + doc_no + " " + str(cnt) + " " + str(score) + " Exp\n")
      else:
        break