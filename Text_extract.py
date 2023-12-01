# Obtención de datos mediante API
# Obtención de IDs a partir de palabras clave

import requests
import xml.etree.ElementTree as ET
import time
import concurrent.futures
import pandas as pd
import requests

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

def buscar_url(parameter, lista):
    #Makes the initial query to get the ID of the related papers using the esearch function
    urlEsearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    paramsEsearch = {
        #Others params such as date, or authors goes here
        'db': 'pmc',
        'retmax' : 1000 ,
        'term': parameter, # term=parameter
        'field': 'abstract',
        'field': 'title'
    }

    try:
        response = requests.get(urlEsearch, params=paramsEsearch)
        response.raise_for_status() #Error control

        # Parse the XML response
        xmlEsearch = ET.fromstring(response.content)

        # Get the IdList field
        id_list_element = xmlEsearch.find(".//IdList")

        # Output the IdList element and its content
        id_list_content = ET.tostring(id_list_element, encoding='unicode')
        IDs = listarIDs(id_list_content)
        urlIDs = [f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC{pmc_id}/ascii"for pmc_id in IDs]
        i = 0
        for url in urlIDs:
            print(i, url)
            i += 1
            lista.append(url)
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

# Aplicación de un filtro para las url funcionales y paralelización

def filtro(url, lista_limpia):
    respuesta = requests.get(url)
    if respuesta.ok:
        lista_limpia.append(url)
    return lista_limpia


lista_velocidad = []
 
print("Running with threads:")
with_threads_start = time.time()

buscar_url('cancer', lista_velocidad)
with concurrent.futures.ThreadPoolExecutor() as executor:
    lista_limpia2 = []
    for url in lista_velocidad:
        executor.submit(filtro, url, lista_limpia2)

print("Threads time:", time.time() - with_threads_start)

#Extracción de texto
#Cristian, esta funcion antes la tenía de manera de que la lista la creaba ella mismo y no hacía falta darsela, pero creo que para paralelizar hay que darsela
def extract_text(API_URL, text):
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

print("Running without threads:")
without_threads_start = time.time()

#con esto es con lo que tengo duda, como coño hace eso por si se tiene que poner así o podría usar un append a una lista
with concurrent.futures.ThreadPoolExecutor() as executor:
    lista_texto_total = []
    for url in lista_limpia2:
        executor.submit(extract_text, url, lista_texto_total)

print("Without threads time:", time.time() - without_threads_start)