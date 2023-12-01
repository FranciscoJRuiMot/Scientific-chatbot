# Obtención de datos mediante API
# Obtención de IDs a partir de palabras clave

import requests
import xml.etree.ElementTree as ET
import pandas as pd

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

    print(termParsed)
    paramsEsearch = {
        'db': database,
        'retmax' : nOfPapers ,
        'term': termParsed,
    }

    try:
        response = requests.get(base, params=paramsEsearch)

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

        


# Aplicación de un filtro para las url funcionales y paralelización
#A comentar esta funcion, como las otras con IN/OUT, te lo dejo a ti que las entiendes mejor que yo
def filtro(url, lista_limpia):
    respuesta = requests.get(url)
    if respuesta.ok:
        lista_limpia.append(url)
    return lista_limpia

#Extracción de texto
#A comentar esta funcion, como las otras con IN/OUT, te lo dejo a ti que las entiendes mejor que yo
def extract_text(API_URL):
    text = []
    respuesta_json = requests.get(API_URL).json()
    df1 = pd.json_normalize(respuesta_json, max_level=1)
    df2 = pd.DataFrame.from_records(df1['documents'])
    df3 = pd.DataFrame.from_records(df2[0])
    df4 = pd.DataFrame.from_records(df3['passages'])
    for i in range(0,df4.size):
        df5 = pd.DataFrame.from_records(df4[i])
        df5_info = pd.DataFrame.from_records(df5['infons'])
        if ((df5_info['section_type'] == 'TITLE') | (df5_info['section_type'] == 'ABSTRACT') | (df5_info['section_type'] == 'INTRO') | (df5_info['section_type'] == 'CONCL')).any():
            df5=df5.convert_dtypes()
            text.append(df5['text'].item())
    return text


