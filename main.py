# client for user to type query
# requirements: support for complex queries using VSM

import vsm
import create_index

# prompt user for a term
print("Please enter a query: ", end="")
query = input()

new_query = []
# preprocess query
for q in query.split():
  q = vsm.word_preprocessing(q)
  if q:
    new_query.append(q)

# calculate cosine similarity score
v = vsm.generate_tfidf_vector(new_query)
scores = vsm.cos_sim_score(v)

# print scores
print("Using Cosine Siliarity...")
for i in range(len(scores)):
  print("The similarity between \"", query, "\" and ", scores[i][1], " is ", scores[i][0], sep='')