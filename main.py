from url_filter import *
from url_finder import *
from text_extractor import *
from question_function import *
import concurrent.futures

#user input of the key words
question = str(input("Please enter your question: "))
filtered_key_words = keys_from_question(question)
print("[BOT] Selected Keywords:", filtered_key_words)
key_urls = buscar_url(filtered_key_words)

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
    print(extracted_main_text)