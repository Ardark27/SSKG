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

def filter_done(pdf_folder_path='data_pdf',
                git_urls_folder_path='data_github_urls',
                no_urls_file='no_urls.txt'):
    # get the files in the folders
    pdf_files = os.listdir(pdf_folder_path)
    git_urls_files = os.listdir(git_urls_folder_path)
    # read no_urls.txt
    with open(no_urls_file, 'r') as f:
        no_urls = f.read().split('\n')
    # remove the extension
    pdf_files = [x.replace('.pdf', '') for x in pdf_files]
    git_urls_files = [x.replace('.txt', '') for x in git_urls_files]
    no_urls_files = [x.replace('.pdf', '') for x in no_urls]
    # convert to set
    pdf_files = set(pdf_files)
    git_urls_files = set(git_urls_files+no_urls_files)
    # get the difference
    not_done = pdf_files.difference(git_urls_files)
    # add the extension
    not_done = [x + '.pdf' for x in not_done]

    return not_done


def pdf_to_git_url(folder_path = 'data_pdf', 
                      output_folder_path = 'data_github_urls'):
    pdf_list = filter_done()
    for file_name in pdf_list:
        print(file_name)
        pdf_path = os.path.join(folder_path, file_name)
        try:
            pdf_data = read_pdf(pdf_path)
            github_urls = look_for_github_urls(pdf_data)
            if github_urls:
                output_path = os.path.join(output_folder_path, file_name.replace('.pdf', '.txt'))
                save_github_urls(github_urls, output_path)
            else:
                print('no urls')
                with open('no_urls.txt', 'a') as f:
                    f.write(file_name + '\n')
        except:
            print('error')
            with open('error.txt', 'a') as f:
                f.write(file_name + '\n')
    return 200

if __name__ == '__main__':
    pdf_to_git_url()