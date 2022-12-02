import pandas as pd
import requests

def get_pdf_url(data_path):
    data = pd.read_csv(data_path)
    return data

def download_pdf(url):
    r = requests.get(url)
    with open('../pdf_info_extractor/data_pdf/' + url.split('/')[-1], 'wb') as f:
        f.write(r.content)

