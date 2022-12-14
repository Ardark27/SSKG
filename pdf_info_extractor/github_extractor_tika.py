from tika import parser
import re
import os

def read_pdf(pdf_path):
    raw = parser.from_file(pdf_path)
    list_pdf_data = raw['content'].split('\n')
    # delete empty lines
    list_pdf_data = [x for x in list_pdf_data if x != '']
    return list_pdf_data

def get_git_urls(text):
    urls_github = re.findall(r'(https?://github.com/\S+)', text)
    urls_gitlab = re.findall(r'(https?://gitlab.com/\S+)', text)
    # create a list with all the urls found
    urls = urls_github + urls_gitlab
    return urls

def look_for_github_urls(list_pdf_data):
    github_urls = []
    for value in list_pdf_data:
        results = get_git_urls(value)
        if results:
            github_urls.extend(results)
    github_urls = [url[:-1] if url[-1] == '.' else url for url in github_urls]
    return github_urls

def save_github_urls(github_urls, output_path):
    with open(output_path, 'w') as f:
        f.write('\n'.join(github_urls))
    return 200

def pdf_to_git_url(folder_path = 'pdf_info_extractor/data_pdf', 
                      output_folder_path = 'pdf_info_extractor/data_github_urls'):
    for file_name in os.listdir(folder_path):
        pdf_path = os.path.join(folder_path, file_name)
        pdf_data = read_pdf(pdf_path)
        github_urls = look_for_github_urls(pdf_data)
        output_path = os.path.join(output_folder_path, file_name.replace('.pdf', '.txt'))
        save_github_urls(github_urls, output_path)
    return 200

if __name__ == '__main__':
    pdf_to_git_url()