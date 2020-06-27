# Reddit Topic Modeling

The “Source Code” folder contains all of the files used in the Reddit data analysis project. The “Comments,” once unzipped, includes a number of JSON files (one for each subreddit) containing the raw comment data from specific subreddits. 

# Main files:
## pushshift_api.py
This script is used to download the comments from individual subreddits 
Please refer here for additional Pushshift.io documenation: 
https://docs.google.com/document/d/171VdjT-QKJi6ul9xYJ4kmiHeC7t_3G31Ce8eozKp3VQ/edit
## preprocesssing.py
Loads in a number of JSON files from the “Comments” directory and returns a single cleaned and formatted CSV file, “reddot_comments_processed.csv.” During this step, we remove emojis and urls from the body text, extracting the data into two additional new columns.
## Topic Modeling.ipynb
This is a jupyter notebook file used for topic modeling. spaCy and Gensim are used in this exploration. The “reddit_comments_processed.csv” is loaded into this file. The end result of this topic modeling a fit LDA model using Gensim and a visual created in pyLDAvis, showing the terms belonging to each topic.

# Supporting files:

All of the other files (e.g. lda_model_all, unigram_sentences_all) are necessary files generated through the phrase modeling and Gensim LDA modeling processes. These files are generated in “Topic Modeling.ipynb.”

## ldavisual_prepared
Generated file to be used by lpyLDAvis within Jupyter Notebook

