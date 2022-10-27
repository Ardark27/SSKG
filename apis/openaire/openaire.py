from email import header
import requests
import xmltodict

UPM = "openorgs____::cad284878801b9465fa51a95b1d779db"
BASE_URL = "https://api.openaire.eu/search/"
def get_openaire_projects(base_url=BASE_URL,org_id=UPM):
    url = base_url + "projects?openaireParticipantID=" + org_id
    response = requests.get(url)
    dict_data = xmltodict.parse(response.content)
    return dict_data

def get_openaire_publications(project_id,base_url=BASE_URL,org_id=UPM):
    url = base_url + "publications?openaireProjectID=" + project_id
    response = requests.get(url)
    dict_data = xmltodict.parse(response.content)
    return dict_data

def get_openaire_software(project_id,base_url=BASE_URL,org_id=UPM):
    url = base_url + "software?openaireProjectID=" + project_id
    response = requests.get(url)
    dict_data = xmltodict.parse(response.content)
    return dict_data

result = get_openaire_projects()

for i in result['response']['results']['result']:
    project = i['header']['dri:objIdentifier']
    publications = get_openaire_publications(project)
    publications_list = publications['response']['results']['result']
    software = get_openaire_software(project)
    print(project)
    print(publications)
    print(software)
