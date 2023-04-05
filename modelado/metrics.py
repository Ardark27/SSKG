import pandas as pd
import numpy as np
from frequent_model import load_data, load_test, model_frequent

def accuracy_score(data:dict, data_train:pd.DataFrame):
    '''
    data: dict key->title, value->github_url
    data_train: pd.DataFrame with the title and github_url
    '''
    # create a list to store the accuracy
    accuracy_list = []
    # loop through the data
    for title, result in data.items():
        result = result.replace('https://github.com/', '').lower()
        result = result.replace('http://github.com/', '')
        # we take only the repo 2 first positions by /
        result = '/'.join(result.split('/')[:2])
        # get the github_url from data_train
        print(title)
        try:
            github_url = data_train.loc[data_train['paper_url_pdf'] == title, 'repo_url'].values[0]
            github_url = github_url.replace('http://github.com/', '').replace('https://github.com/', '').lower()
        except:
            continue
        print(result, github_url)
        # check if the result is equal to the github_url
        if result == github_url:
            # append 1 to the accuracy_list
            accuracy_list.append(1)
        else:
            # append 0 to the accuracy_list
            accuracy_list.append(0)
    # return the accuracy
    return np.mean(accuracy_list), accuracy_list

if __name__ == "__main__":
    data = load_data()
    data_train = load_test()
    data = model_frequent(data)
    print(accuracy_score(data, data_train)[0])