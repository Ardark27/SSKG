import json

def load_data(path):
    with open(path) as f:
        return json.load(f)

def extract_dois(data):
    dois = []
    for item in data["hits"]:
        dois.append('https://doi.org/'+item['doi'])
    return dois

def save_dois(dois, path):
    with open(path, 'w') as f:
        json.dump(dois, f, indent=4)
    
    return len(dois)

def main():
    data = load_data('apis/zenodo/publication.json')
    dois = extract_dois(data)
    count = save_dois(dois, 'apis/zenodo/zenodo_dois.json')
    print('Saved {} dois'.format(count))

if __name__ == '__main__':
    main()