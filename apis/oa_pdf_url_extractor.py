import pandas as pd
import requests
import json

def create_unpaywall_url(data):
    """
    data: dataframe with doi column that contains the doi url
    """
    # Get the dois_id from the doi column
    data['dois_id'] = data['doi'].str.split('org/').str[-1]
    # we are going to delete the ones that have figshare in the doi_id, due to the fact that they are not in the unpaywall api
    data = data[~data['dois_id'].str.contains('figshare')]
    # we are going to delete the ones that have zenodo in the doi_id, due to the fact that they are not in the unpaywall api
    data = data[~data['dois_id'].str.contains('zenodo')]
    # we are going to negociate pdf content with the unpaywall api
    data['unpaywall_url'] = 'https://api.unpaywall.org/v2/' \
                                + data['dois_id'] \
                                + '?email=nick.haupka@gmail.com'
    return data

def get_unpaywall_pdf_url(data):
    pdf_url_list = []
    total_urls = len(data)
    for i in range(total_urls):
        try:
            
            r = requests.get(data['unpaywall_url'].iloc[i])
            pdf_url = r.json()['best_oa_location']['url_for_pdf']
            pdf_url_list.append(pdf_url)
            print(f'{i} of {total_urls} satisfied')
        except:
            print(f'{i} of {total_urls} non satisfied')
            pdf_url_list.append(None)
    
    data['pdf_url'] = pdf_url_list

    return data

def main():
    # Read the csv file
    data = pd.read_csv('dois_not_arxiv.csv')
    # Create the unpaywall url
    data = create_unpaywall_url(data)
    # Get the pdf url
    data = get_unpaywall_pdf_url(data)
    # Save the csv file
    data.to_csv('doi_not_arxiv_with_pdf_url.csv', index=False)


if __name__ == '__main__':
    main()