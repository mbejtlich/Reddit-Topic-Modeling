# This script batch aggregates several subreddit JSON files and exports a cleaned and structured CSV file.
# URL and emoji extraction is performed to the text feild, and the new features are added to a new column.

# Import modules
import os, json
import pandas as pd
import re
import emoji
import numpy as np
import datetime

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def filenames(directory):
    """ This funtion returns a list of all files names in a directory
    dictionary_path - directory name (e.g. comments)
    outputs:
    content - [{'author':'matt','author_flair_background_color': None},{'author':steph,'author_flair_background_color': None}]
    """
    # onlyfiles = [f for f in listdir(directory+'/') if isfile(join(directory+'/', f))]

    list_filenames = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith((".json")):
                list_filenames.append(name)

    return list_filenames

def load_json(directory,document):
    """ This function reads a json file line by line and returns a list of documents as dictionary objects
    dictionary_path - Path to json file
    outputs:
    content - [{'author':'matt','author_flair_background_color': None},{'author':steph,'author_flair_background_color': None}]
    """
    data = []
    with open(directory+'/'+document) as f:
        for line in f:
            x = json.loads(line)
            data.append(x)

    return data

def convert_dataframe(subreddit_docs):
    """ This function reads in a list of dictionary objects and outputs a pandas dataframe
    subreddit_docs - List of dictionary objects representing documents of subreddit
    outputs:
    content - Subreddit dataframe object
    """

    # remove \r\r comments
    regex = re.compile("\\r\\r")
    subreddit_docs = [docs for docs in subreddit_docs if not re.search(regex,docs['body'])]

    df = pd.DataFrame(subreddit_docs)

    df = df[['id',
             'subreddit',
             'author',
             'body',
             'created_utc',
             'score',
             'subreddit_id',
             'parent_id',
             'link_id']]

    df.rename(columns={'body': 'body_text', 'id': 'document_id'}, inplace=True)

    return df

def clean(df):
    """ This function reads in a list of dictionary objects and outputs a pandas dataframe
    subreddit_docs - List of dictionary objects representing documents of subreddit
    outputs:
    content - Subreddit dataframe object
    """

    # drop NaN
    df = df.dropna(how='any')
    # drop '[removed]' text
    df = df[df.body_text != '[removed]']

    newline_match = re.compile(r'\r|\n')
    url_match = re.compile(r'(http\S+)')
    hashmarks_match = re.compile(r'"')

    # replace \n or \r with ''
    df['body_text'] = df['body_text'].str.replace(newline_match, ' ')

    # strip " from all strings
    df['body_text'] = df['body_text'].str.replace(hashmarks_match, '')

    # extract URL and store in new column
    df['urls'] = df['body_text'].str.findall(url_match)

    # replace url with 'URLtag'
    df['body_text'] = df['body_text'].str.replace(url_match, 'URLtag')

    # # add emoji patterns to new column, 'emoji'
    df['emoji'] = df['body_text'].map(extract_emojis)
    # df.emoji = df.emoji.fillna('')

    #remove emoji patterns from body, 'emoji'
    df['body_text'] = df['body_text'].map(remove_emojis)

    # df['body_text'] = df.apply(lambda x: x.body_text.str.replace([c for c in x.emoji], ""), axis=1)
    # df['body_text'] = df['body_text'].str.replace(r'[^\s]+', '')

    return df

def extract_emojis(str):
    return [c for c in str if c in emoji.UNICODE_EMOJI]

def remove_emojis(str):
    return ''.join([c for c in str if c not in emoji.UNICODE_EMOJI])

# def clean_text(rgx_list, text):
#     output = text
#     for rgx_match in rgx_list:
#         output = re.sub(rgx_match, '', text)
#     return output

def export_csv(df):
    """ This function reads in main dataframe containing all subreddits and exports a single CSV file
    subreddit_docs - Pandas dataframe object
    """
    # print(df.shape[0])
    df['body_text'] = df['body_text'].astype(str)
    print(df.body_text.dtype)
    df.to_csv('reddit_comments_processed.csv', encoding='utf-8', index=False)
    print(df.shape[0])

def main():
    directory = 'Comments'
    files=filenames(directory)

    df_list = []
    x = 1
    for subreddit_file in files:
        print("{} — {}".format(x, subreddit_file))
        subreddit_docs = load_json(directory,subreddit_file)
        subreddit_df = convert_dataframe(subreddit_docs)
        print(subreddit_df.shape[0])
        df_list.append(subreddit_df)
        x=x+1

    main_df = pd.concat(df_list, ignore_index=True)

    if isinstance(main_df, pd.DataFrame):
        print(type(main_df))
        main_df = clean(main_df)
        export_csv(main_df)

if __name__ == '__main__':
    main()