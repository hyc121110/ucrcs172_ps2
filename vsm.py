# Part A: 
# parse each doc from dir
# for each doc, tokenize doc into words, remove stop words, lowercase each token
import os
import string
import math

from numpy import zeros
from numpy import dot
from numpy.linalg import norm

from nltk.stem import PorterStemmer
from collections import defaultdict

path = os.getcwd()
ps = PorterStemmer()

word_freq = defaultdict(int) # count for terms in all documents
posting_index = dict() # dictionary with key "term" and value (# docs in which term occurs, [posting-list])
document_index = dict() # dictionary with key "doc id" and value "num of terms in doc"

# main
def main():
  # prompt user for a directory
  createIndex("\\data\\ap89_collection")

  # prompt user for a term
  print("Please enter a query: ", end="")
  query = input()
  termLookup(query)

# each doc begins with <doc> ends with </doc>
# doc id: <DOCNO>
# text processed: <text> </text>
def createIndex(directory):
  doc_start = False
  doc_number = False
  text_start = False

  with open('stoplist.txt') as f1:
    stop_words = f1.read()
    # define new path
    new_path = path + directory
    # open ap89_collection
    with open(new_path, "r") as f:
      # split words
      words = [word for line in f for word in line.split()]
      for word in words:
        # check <DOC>
        if word == "<DOC>":
          # initialize variables for the doc
          doc_start = True
          docID_freq = defaultdict(int) # temporary dictionary for posting-list
          num_terms_in_doc = 0  # count no. of terms in doc
          word_freq_in_cur_doc = defaultdict(int) # term frequency count for each file
          continue
        # check <DOCNO>
        if word == "<DOCNO>":
          doc_number = True
          continue
        # if doc_number is True, filename = doc_id
        if doc_number:
          fn = word
          # done with doc_id
          doc_number = False
          continue
        # check <text>
        if word == "<TEXT>":
          text_start = True
          continue
        # check </text>
        if word == "</TEXT>":
          text_start = False
          continue        
        # check </DOC>
        if word == "</DOC>":
          doc_start = False
        
        if text_start:
          # one liner to remove punctuation and lowercase each token            
          word = word.translate(str.maketrans('', '', string.punctuation)).lower()
          # check if word is a stop word and any numbers in string
          if word not in stop_words and not any(str.isdigit(c) for c in word):
            num_terms_in_doc += 1
            # apply stemming
            word = ps.stem(word)
            docID_freq[word] += 1

            if word in word_freq:
              # word has appeared before, just increment counters
              word_freq[word] += 1
              word_freq_in_cur_doc[word] += 1
            else:
              # initialize values of counters 
              word_freq[word] = 1
              word_freq_in_cur_doc[word] = 1
              posting_index[word] = (1, list())
        
        if not doc_start:
          # after all words within <DOC> </DOC> are counted 
          document_index[fn] = num_terms_in_doc
          for term in docID_freq.keys():
            posting_index_list = posting_index[term][1] # a list which contains tuples of doc id and freq of word in doc
            posting_index_list.append((fn, word_freq_in_cur_doc[term])) # append doc id and freq of word in doc
          
  # count the total number of items in posting_index
  for term in posting_index.keys():
    doc_cnt = posting_index[term][1]
    # reset the value of "num docs in which term occurs" as number of items in the list
    posting_index[term] = (len(doc_cnt), posting_index[term][1])

def termLookup(query):
  # print tf-idf of query for each doc
  # if term not found, print "No Match"

  # one liner to remove punctuation and lowercase each token            
  word = query.translate(str.maketrans('', '', string.punctuation)).lower()
  # apply stemming
  word = ps.stem(word)

  # check if query in posting_index
  if word in posting_index.keys():
    # calculate tf-idf
    # first calculate term frequency tf in each document
    for doc in document_index.keys():
      freq = 0
      posting_list = posting_index[query][1]
      # find doc id
      for i in range(len(posting_list)):
        if posting_list[i][0] == doc:
          # found doc id, just need the freq
          freq = posting_list[i][1]
          break
      # calculate tf
      tf = freq / document_index[doc]
      # now calculate idf
      N = len(document_index)
      n_k = posting_index[query][0]
      idf = 1 + math.log(N)/(n_k+1)
      # calculate tf-idf
      tfidf = tf * idf
      print("TF-IDF for", doc, "is", tfidf)
  else:
    # no match
    print("No Match")

def removeStopWords(list):
  pass

def cosineSim(d1, d2):
  v1 = docVec(d1)
  v2 = docVec(d2)
  return float(dot(v1,v2) / (norm(v1) * norm(v2)))



if __name__ == "__main__":
  main()