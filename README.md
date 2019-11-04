# CS172_PS2

## Name

Ho Yee Chan

## Dependencies

- nltk
- numpy

## Description

There are four python scripts in the directory.

- main.py: the client where you can type complex queries and the programs returns the cosine similarity scores between the query and the documents.

- vsm.py: script calculating the cosine similarity scores between the query and the documents

- lm-unigram.py: script calculating the maximum likehood estimates between query and document with Laplace smoothing

- create_index.py: script generating the document index and posting index based on ap89_collection

## How to run

### Part 1: Extension of PS1

Type "python main.py" to start the script. Type in complex queries (>1 word) and the program will print out the cosine similarity scores between the query and the documents.

### Part 2: Query Execution (VSM)

To run the queries in the file query_list.txt, type "python ./vsm.py data query_list.txt result_vsm.txt" in the terminal from the directory where "CS172_PS2.pdf" is located. The file "result_vsm.txt" will be generated which contains the top 50 document relevant score between a query and a given document.

### Part 3: Language Model

To run the language model, type "python ./lm-unigram.py data query_list.txt result_lm.txt" in the terminal from the directory where "CS172_PS2.pdf" is located. The file "result_lm.txt" will be generated which contains the top 50 document relevant score between a query and a given document.

### Part 4: Evaluation

To evaluate rankings, type "data/trec_eval.pl -q data/qrels.txt result_vsm.txt" for evaluating VSM and " data/trec_eval.pl -q data/qrels.txt result_lm.txt" for evaluating the Language Model.
