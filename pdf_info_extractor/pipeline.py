from grobid.grobid_client.grobid_client import GrobidClient
from github_extractor import xml_to_github_url
import os

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
             github_urls_output_path="data_github_urls"):
    
    #os.system(('docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.1')) --> no funciona se queda en el proceso de creación del contenedor
    pdf_to_xml(pdf_path, xml_output_path)
    xml_to_github_url(xml_output_path, github_urls_output_path)

    return 200


if __name__ == "__main__":
    print(pipeline_process_pdf())