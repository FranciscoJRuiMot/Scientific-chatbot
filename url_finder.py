# Obtención de datos mediante API
# Obtención de IDs a partir de palabras clave

import requests
import xml.etree.ElementTree as ET

#Makes the initial query to get the ID of the related papers using the esearch function
#IN:
#   String/List term: term/terms to search for in the papers #In the future it will be a list of parameters for different options of the search 
#   database
#   nOfPapers
#   field
#   publishDate
#OUT:
#   paperUrls: list of URLs of the papers selected according to the parameters
def buscar_url(term,database="pmc",nOfPapers=1000,field="mesh",publishDate=None):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    #Parses the term/terms to apply the selected field
    if isinstance(term, str):
        termParsed = (f"{term}[{field}]")
    elif isinstance(term, list):
        termParsed = (f"{term.pop(0)}[{field}]")
        if len(term) >= 1:      
            for t in term:
                termParsed += (f"+AND+{t}[{field}]")
    else:
        raise ValueError(f"{type(term)} is an unsupported type for term")
    
    #Handles the case where publishDate is given
    if publishDate != None:
        termParsed += (f"+AND+{publishDate}[pdat]")

    urlSearch = f"{base}?db={database}&retmax={nOfPapers}&term={termParsed}"

    try:
        response = requests.get(urlSearch)

        # Parse the XML response
        xmlEsearch = ET.fromstring(response.content)

        # Get the IdList field
        id_list_element = xmlEsearch.find(".//IdList")
        
        # Output the IdList element and its content
        id_list_content = ET.tostring(id_list_element, encoding='unicode')
        IDs = listarIDs(id_list_content)
        paperUrls = [f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC{pmc_id}/ascii"for pmc_id in IDs]
        return paperUrls
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")


#Get the IDs of the given esearch response
#IN:
#   list_content: the API's json response to a esearch query by the parameters given
#OUT:
#   IDs: list of IDs of the papers we requested
def listarIDs(list_content):
    try:
        root = ET.fromstring(list_content)
        id_elements = root.findall(".//Id")
        # Extract and return the ids as an array
        IDs = [id_element.text for id_element in id_elements]
        return IDs

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

        
