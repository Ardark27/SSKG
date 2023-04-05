from somef_utils import load_json
import os
import arxiv
import requests
import jaro

def get_title_somef(path):
    # get description and full title
    data = load_json(path)
    try:
        return data['description']+data['full_title']
    except:
        return []

def get_title(doi):
    try:
        search = arxiv.Search(id_list=[doi])
        paper = next(search.results())
        return paper.title
    except:
        try:
            url_base = "https://api.crossref.org/works/"
            # if doi has more than 1 _ replace first _ with /
            doi = doi.replace('_', '/', 1)
            response = requests.get(url_base + doi)
            reponse_json = response.json()
            return reponse_json['message']['title'][0]
        except:
            return None

def get_best_jaro(path):
    #get description path list
    file_path = [os.path.join(path,i) for i in os.listdir(path)]
    #get description
    description = [get_title_somef(i) for i in file_path]
    #get title
    title = get_title(path.split('\\')[-1])
    #get jaro for each description
    best_jaro = 0
    solucion = None
    for index,value in enumerate(description):
        for j in value:
            title_assert = j['result']['value']
            if title_assert != None and title != None:
                metric_jaro = jaro.jaro_winkler_metric(title_assert, title)
                if metric_jaro > best_jaro:
                    best_jaro = metric_jaro
                    solucion = file_path [index]
    return solucion, best_jaro

