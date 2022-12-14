from grobid.grobid_client.grobid_client import GrobidClient
from github_extractor_grobid import xml_to_github_url
from somef_extractor import somef_pipeline
from github_extractor_tika import pdf_to_git_url, output_formatter
import os
import tika

def pdf_to_xml(pdf_path="data_pdf", output_path="data_xml"):
    client = GrobidClient(config_path="grobid/config.json")
    client.process(
        "processFulltextDocument", 
        input_path=pdf_path, 
        output=output_path,  
        force=True, verbose=True)
    return 200

def pipeline_process_pdf(pdf_path="data_pdf", 
             xml_output_path="data_xml", 
             github_urls_output_path="data_github_urls",
             somef_output_folder_path="data_somef",
             use_grobid=False):
    if use_grobid:
        #os.system(('docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.1')) --> no funciona se queda en el proceso de creación del contenedor
        pdf_to_xml(pdf_path, xml_output_path)
        xml_to_github_url(xml_output_path, github_urls_output_path)
        parser = 'grobid'
        parser_version = '0.7.1'
    else:
        pdf_to_git_url(pdf_path, github_urls_output_path)
        parser = 'tika'
        parser_version = tika.__version__
    output_formatter(github_urls_output_path, parser=parser, parser_version=parser_version)
    somef_pipeline(github_urls_output_path,somef_output_folder_path)

    return 200


if __name__ == "__main__":
    print(pipeline_process_pdf())