from url_filter import *
from text_extractor import *
import concurrent.futures

#filtering url

with concurrent.futures.ThreadPoolExecutor() as executor:
    filtered_urls_list = []
    for url in key_urls:
        executor.submit(url_filter, url, filtered_urls_list)

#extracting text from papers

with concurrent.futures.ThreadPoolExecutor() as executor:
    extracted_main_text = []
    futures = [executor.submit(extract_text, url) for url in filtered_urls_list]
    extracted_main_text = [future.result() for future in futures]