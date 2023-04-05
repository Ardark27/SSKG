import os
import pandas as pd

def load_data(directory = 'corpus/papers_with_code_github'):
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

def load_test(path ='corpus/papers_with_code.csv'):
    # load the columns paper_url_pdf and repo_url as strings
    data = pd.read_csv(path, usecols=['paper_url_pdf','repo_url'], dtype=str)
    data = data.dropna()
    # apply title.replace('/', '_').replace(':', ' ').replace('?','')
    data['paper_url_pdf'] = data['paper_url_pdf'].apply(lambda x: x.split('/')[-1].replace('.pdf','').replace('/', '_').replace(':', ' ').replace('?',''))
    return data

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

    # nombre del repo aparece en el titulo del paper, asumimos tener el titulo del paper
    # nombre del repo aparece en el abstract del apaper, asumimos tener el abstract del paper
    # contributors del repo, con los autores del paper, asumimos tener los autores del paper
        # query graphql para los contributres del repo
