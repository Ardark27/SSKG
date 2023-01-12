import os
import pandas as pd

def load_data(directory = 'corpus/papers_with_code_automated'):
    # charge the data
    files_list = os.listdir(directory)
    # filter the files with .txt extension
    files_list = [file for file in files_list if file.endswith('.txt')]
    # create a list to store the data
    data_dict = {}
    # loop through the files
    for file in files_list:
        # open the file
        with open(os.path.join(directory, file), 'r') as f:
            # read the file with multiple lines
            data = f.read().split('\n')
            # append the data
            data_dict[file.replace('.txt', '')] = data
    return data_dict

def load_test(path = 'corpus/papers_with_code.xlsx'):
    # load the data
    data = pd.read_excel(path)
    data_train = data.loc[:,['title','github_url']]
    # apply title.replace('/', '_').replace(':', ' ').replace('?','')
    data_train['title'] = data_train['title'].apply(lambda x: x.replace('/', '_').replace(':', ' ').replace('?',''))
    return data_train

def model_frequent(data:dict):
    # create a dictionary to store the data
    data_dict = {}
    # loop through the data
    for key, value in data.items():
        # create a dictionary to store the frecuency of each repo
        frecuency_dict = {}
        # loop through the repos
        for repo in value:
            # check if the repo is in the dictionary
            if repo in frecuency_dict:
                # increase the frecuency
                frecuency_dict[repo] += 1
            else:
                # add the repo to the dictionary
                frecuency_dict[repo] = 1
        # get the most frecuent repo
        most_frecuent = max(frecuency_dict, key=frecuency_dict.get)
        # add the most frecuent repo to the data
        data_dict[key] = most_frecuent
    # return the data
    return data_dict