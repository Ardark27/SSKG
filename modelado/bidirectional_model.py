import os
import json
from somef_utils import find_doi

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def is_bidirectional(file_path: str):
    try:
        data = load_json(file_path)
    except json.decoder.JSONDecodeError:
        print("Error in file: ", file_path)
        return False
    doi = find_doi(data)
    folder = os.path.basename(os.path.dirname(file_path))
    file = os.path.basename(file_path)
    if doi:
        doi_pdf = folder.replace('.txt','')
        doi_pdf = doi_pdf.split('v')[0]
        print('DOI: ', doi, 'DOI PDF: ', doi_pdf, 'file: ', file_path)
        
        if doi == doi_pdf:
            print("Yes this is bidirectional", doi, file.replace('.json','').replace('_', '/'))
            return (doi, file.replace('.json','').replace('_', '/'))  
    else:
        print("Not found doi in file: ", file_path)
        return False

def execute_bidirectional(folder_path: str):
    folders = os.listdir(folder_path)
    dois_found = {}
    for folder in folders:
        somef_folder_path = os.path.join(folder_path, folder)
        files = os.listdir(somef_folder_path)
        for file in files:
            file_path = os.path.join(somef_folder_path, file)
            result = is_bidirectional(file_path)
            if result:
                # check if the doi is already in the dict
                if result[0] in dois_found.keys():
                    # append the new path
                    dois_found[result[0]].append(result[1])
                    continue
                dois_found[result[0]] = [result[1]]
    return dois_found



if __name__=="__main__":
    print(execute_bidirectional('corpus/papers_with_code_somef'))
    print(execute_bidirectional('../pdf_info_extractor/data_somef'))