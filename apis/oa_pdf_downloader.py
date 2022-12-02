import pandas as pd
import numpy as np
import requests

def get_pdf_url_and_doi(data_path):
    data = pd.read_csv(data_path)
    return data["pdf_url"], data["dois_id"]


def download_pdf(url,name_of_pdf):
    r = requests.get(url)
    # replace dois_id / with _
    name = name_of_pdf.replace('/','_')+ '.pdf'
    with open('../pdf_info_extractor/data_pdf/' + name, 'wb') as f:
        f.write(r.content)

def main():
    oa_url,doi_id = get_pdf_url_and_doi('dois_not_arxiv_with_pdf_url.csv')

    for url,doi in zip(oa_url,doi_id):
        #check if url is not empty
        if url is not np.nan:
            print('Downloading: ', url)
            download_pdf(url,doi)
        break #remove this line to download all the pdfs

if __name__ == '__main__':
    main()

