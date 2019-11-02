# Part A: 
# parse each doc from dir
# for each doc, tokenize doc into words, remove stop words, lowercase each token
import os
import string

from nltk.stem import PorterStemmer
ps = PorterStemmer()

from collections import defaultdict

path = os.getcwd()

word_freq = defaultdict(int) # count for terms in all documents
posting_index = dict() # dictionary with key "term" and value (# docs in which term occurs, [posting-list])
document_index = dict() # dictionary with key "doc id" and value "num of terms in doc"

# Part 1
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
        
        # <text>
        if text_start:
          # one liner to remove punctuation and lowercase each token
          word = remove_punctuation_lowercase(word)
          # check if word is a stop word and any numbers in string
          if word not in stop_words and not any(str.isdigit(c) for c in word):
            num_terms_in_doc += 1
            # apply stemming
            word = stemming(word)
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

# function to remove punctuation from words and lowercase them
def remove_punctuation_lowercase(word):
  return word.translate(str.maketrans('', '', string.punctuation)).lower()

# function to apply stemming
def stemming(word):
  return ps.stem(word)

# function to return queries as list of lists
def processQueries(full_path):
  with open(full_path) as fp:
    lines = fp.readlines()
    for idx, line in enumerate(lines):
      lines[idx] = line.split()
  return lines
  
# main
createIndex("\\data\\ap89_collection")