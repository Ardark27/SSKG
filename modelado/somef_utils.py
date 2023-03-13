import os
import json
import bibtexparser

def cff_parser(cite_list: list):
    '''
    Parse the citation list of a cff file given by somef
    '''
    # remove empty elements
    cite_list = [element for element in cite_list if element != '']
    # replace " by ''
    cite_list = [element.replace('"', '') for element in cite_list]
    parsed_dict = {}
    for element in cite_list:
        if element.count(':') > 1:
            key = element.split(':')[0].strip()
            value = ':'.join(element.split(':')[1:]).strip()
            parsed_dict[key] = value
        else:
            try:
                key, value = element.split(':')
                key = key.strip()
                value = value.strip()
            except ValueError:
                key = element.split(':')[0].strip()
                value = ''
            parsed_dict[key] = value
    return parsed_dict

def bibtex_parser(cite_list: list):
    '''
    Parse the citation list of a bibtex ref given by somef
    '''
    # parse first element
    cite_list[0] = cite_list[0].replace('{','=')
    # remove @ and {}
    cite_list = [element.replace('@', '').replace('{', '').replace('}', '') for element in cite_list]
    # remove empty elements
    cite_list = [element for element in cite_list if element != '']
    # strip elements
    cite_list = [element.strip() for element in cite_list]
    # remove final comma
    cite_list = [element[:-1] if element[-1] == ',' else element for element in cite_list]
    parsed_dict = {}
    for element in cite_list:
        if element.count('=') > 1:
            key = element.split('=')[0].strip()
            value = '='.join(element.split('=')[1:])
            parsed_dict[key] = value
        else:
            try:
                key, value = element.split('=')
                key = key.strip()
                value = value.strip()
            except ValueError:
                key = element.split('=')[0].strip()
                value = ''
            parsed_dict[key] = value
    return parsed_dict

def text_excerpt_parser(cite_list: list):
    # remove @ and {}
    cite_list = [element.replace('@', '').replace('{', '').replace('}', '') for element in cite_list]
    # strip elements
    cite_list = [element.strip() for element in cite_list]
    # remove empty elements
    cite_list = [element for element in cite_list if element != '']
    # remove final comma
    cite_list = [element[:-1] if element[-1] == ',' else element for element in cite_list]
    
    parsed_dict = {}
    for element in cite_list:
            if element.count('=') == 1:
                try:
                    key, value = element.split('=')
                    key = key.strip()
                    value = value.strip()
                except ValueError:
                    key = element.split('=')[0].strip()
                    value = ''
                parsed_dict[key] = value
    
    return parsed_dict

def find_doi(somef_data: dict):
    '''
    Find the doi in somef data 
    '''
    try:
        data = somef_data['citation']
    except KeyError:
        return False
        
    for cite in data:
        try:
            if cite['result']['format'] == 'cff':
                cff = cff_parser(cite['result']['value'].split('\n'))
                doi_find = cff['doi'].replace('https://doi.org/','').replace('10.48550/arxiv.','').replace('10.48550/ARXIV.','').replace('/','_')
                return doi_find
            elif cite['result']['format'] == 'bibtex':
                try:
                    bibtex = bibtexparser.loads(cite["result"]["value"]).entries[0]
                except:
                    print('Error parsing bibtex')
                    bibtex = bibtex_parser(cite['result']['value'].split('\n'))
                doi_find = bibtex['doi'].replace('https://doi.org/','').replace('10.48550/arxiv.','').replace('10.48550/ARXIV.','').replace('/','_')
                return doi_find
            elif cite['result']['type'] == 'Text_excerpt':
                text = text_excerpt_parser(cite['result']['value'].split('\n'))
                doi_find = text['doi'].replace('https://doi.org/','').replace('10.48550/arxiv.','').replace('10.48550/ARXIV.','').replace('/','_')
                return doi_find
        except KeyError:
            continue
    return False