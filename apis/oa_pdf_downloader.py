import pandas as pd
import numpy as np
import requests
import os

def get_pdf_url_and_doi(data_path):
    data = pd.read_csv(data_path)
    return data["pdf_url"], data["dois_id"]

def generate_downloaded_list(file_tracking='download_trace.txt' ,folder_pdfs='../pdf_info_extractor/data_pdf/'):
    downloaded_list = os.listdir(folder_pdfs)
    with open(file_tracking, 'w') as f:
            f.write('\n'.join(downloaded_list))

def check_downloaded_list(name,file_path):
    with open(file_path) as f:
        downloaded_list = f.readlines()
    downloaded_list = [x.strip() for x in downloaded_list]
    if name.strip() in downloaded_list:
        return True
    else:
        return False


def download_pdf(url,name_of_pdf):

    # replace dois_id / with _
    name = name_of_pdf.replace('/','_')+ '.pdf'
    if check_downloaded_list(name,'download_trace.txt'):
        print('already downloaded')
        return 404
    try:
        r = requests.get(url)
        # Save the pdf
        with open('../pdf_info_extractor/data_pdf/' + name, 'wb') as f:
            f.write(r.content)
        # make a file for downloading trace
        with open('download_trace.txt', 'a') as f:
            f.write(f'\n{name}')
        
        return 200
    except:
        # make a file for the error trace
        with open('error_trace.txt', 'a') as f:
            f.write(f'\n{url}')
        return 404

def download_oa():
    oa_url,doi_id = get_pdf_url_and_doi('dois_not_arxiv_with_pdf_url.csv')
    for url,doi in zip(oa_url,doi_id):
        #check if url is not empty
        if url is not np.nan:
            print('Downloading: ', url)
            download_pdf(url,doi)
            break #remove this line to download all the pdfs
if __name__ == '__main__':
    generate_downloaded_list()
    download_oa()

