import xmltodict
import re
import os

def read_xml(xml_path):
    with open(xml_path, 'r', encoding='utf-8') as f:
            xml_dict = xmltodict.parse(f.read())
    return xml_dict

def recursive_dict_iterator(data):
    for key, value in data.items():
        if isinstance(value, dict):
            yield from recursive_dict_iterator(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    yield from recursive_dict_iterator(item)
                else:
                    yield key, item
        else:
            yield key, value

def get_github_urls(text):
    # problem with line break
    urls = re.findall(r'(https?://github.com/\S+)', text)
    return urls

def look_for_github_urls(data):
    github_urls = []
    for key, value in recursive_dict_iterator(data):
        if type(value) == str:
            print(value)
            results = get_github_urls(value)
            if results:
                github_urls.extend(results)
    # we dont remove duplicates due to the fact that we will use it
    # github_urls = list(set(github_urls))
    # remove . at the end of the url
    github_urls = [url[:-1] if url[-1] == '.' else url for url in github_urls]
    # remove https://github.com/kermitt2/grobid from the list
    github_urls = [url for url in github_urls if url != 'https://github.com/kermitt2/grobid']
    
    return github_urls

def extract_github_urls(xml_path):
    data = read_xml(xml_path)
    github_urls = look_for_github_urls(data)
    return github_urls

def save_github_urls(github_urls, output_path):
    with open(output_path, 'w') as f:
        f.write('\n'.join(github_urls))
    return 200

def xml_to_github_url(folder_path = 'pdf_info_extractor/data_xml', output_folder_path = 'pdf_info_extractor/data_github_urls'):
    for file_name in os.listdir(folder_path):
        xml_path = os.path.join(folder_path, file_name)
        github_urls = extract_github_urls(xml_path)
        output_path = os.path.join(output_folder_path, file_name.replace('.xml', '.txt'))
        save_github_urls(github_urls, output_path)
    return 200
# Problema encontrado:
# Grobid no lee algunas urls de github, por ejemplo:
# - https://github.com/blue-yonder/di-csv2xml. en el pdf 1-s2.....

if __name__ == "__main__":
    xml_to_github_url()