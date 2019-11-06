import create_index
import os
import sys
import math

# posting index
posting_index = create_index.posting_index
# document index
document_index = create_index.document_index
# word freq
unique_words = create_index.unique_words

# main
user_path = os.getcwd() # get current path

# specify arguments
path = sys.argv[1] # directory
f = sys.argv[2] # query list
result_f = sys.argv[3] # write to result
full_path = user_path + "\\" + path + "\\" + f

# delete existing result file if exists
if os.path.exists(user_path + "\\" + result_f):
  os.remove(result_f)

# process queries
queries = create_index.processQueries(full_path)

# function calculating p_laplace, returning lists of ps and doc number
def p_laplace(word, doc):
  # formula: (tf + 1) / (len(d) + V)
  tf = 0
  # find doc number in posting index. If word not found, freq = 0
  if word in posting_index:
    posting_list = posting_index[word][1]
    for tup in posting_list:
      if tup[0] == doc:
        tf = tup[1]
        break

  numerator = tf + 1
  # V: unique terms in one document
  denominator = document_index[doc] + len(unique_words)

  return numerator / denominator

# function to preprocess word
def word_preprocessing(q):
  if q not in stop_words and not any(str.isdigit(c) for c in q):
    # word preprocessing
    q = create_index.remove_punctuation_lowercase(q)
    q = create_index.stemming(q)
    return q
  # return empty string if not satisfy
  return ""

# a list to track probabilities 
docs_prob = list()


with open('stoplist.txt') as f1:
  stop_words = f1.read()
  for query in queries:
    # check if query is a number
    first = True
    # remove all stopwords, remove punctuation, lowercase and stem the word first
    new_query = list()
    # check if number is a query number
    first = True
    # get rid of redundant words from query
    for idx, q in enumerate(query):
      if any(str.isdigit(c) for c in q) and idx == 0:
        # query number
        q_num = q.rstrip('.') # remove the period
        first = False
      else:
        # word preprocessing
        q = word_preprocessing(q)
        if q:
          new_query.append(q)
    
    # laplace smoothing
    scores = list()
    for doc in document_index:
      score = 0
      for q in new_query:
        score += math.log(p_laplace(q, doc))
      scores.append((score, doc))
    # sort scores in descending order
    scores = sorted(scores, reverse=True)

    # only top 20 results are needed
    max_scores = 50
    cnt = 0
    for score, doc_no in scores:
      if cnt < max_scores:
        # write result to file
        # <query number> Q0 <docno> <rank> <score> Exp
        cnt += 1
        with open(result_f, "a") as myfile:
          myfile.write(q_num + " Q0 " + doc_no + " " + str(cnt) + " " + str(score) + " Exp\n")
      else:
        break