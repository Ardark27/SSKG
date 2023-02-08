import os

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return 200

def read_file(file):
    # read it line by line
    with open(file, 'r') as f:
        text = f.readlines()
    # remove \n
    text = [line.replace('\n', '') for line in text]

    return text

def execute_somef_extractor(name, folder_path = 'corpus/papers_with_code_github', somef_output_folder_path = 'corpus/papers_with_code_somef'):
    # create a folder to store the output of the extractor
    output_folder_path = os.path.join(somef_output_folder_path, name.replace('.txt',''))
    print(output_folder_path)
    create_folder(output_folder_path)
    # read the file with the urls
    file_path = os.path.join( folder_path, name)
    print(file_path)
    urls = read_file(file_path)
    urls = list(set(urls))
    # execute the extractor
    for url in urls:
        output_file_path = os.path.join(output_folder_path, url.replace('http://gitlab.com/','').replace('https://gitlab.com/','').replace('http://github.com/','').replace('https://github.com/','').replace('/','_')+'.json')
        command = f"somef describe -r {url} -o {output_file_path} -t 0.8"
        print(command)
        os.system((command))
    
    return 200

def somef_pipeline(folder_path = 'corpus/papers_with_code_github', somef_output_folder_path = 'corpus/papers_with_code_somef'):
    files = os.listdir(folder_path)
    for file in files:
        print(file)
        execute_somef_extractor(file, folder_path, somef_output_folder_path)
    return 200

if __name__ == "__main__":
    print(somef_pipeline())