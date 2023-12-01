import time
from text_extract import *
 

#---------------------Threads--------------------------------#

print("Running with threads:")
with_threads_start = time.time()

lista_velocidad = buscar_url('cancer')
with concurrent.futures.ThreadPoolExecutor() as executor:
    lista_limpia = []
    for url in lista_velocidad:
        executor.submit(filtro, url, lista_limpia)

print("Threads time:", time.time() - with_threads_start)

#---------------------Threadsless----------------------------#

print("Running without threads:")
without_threads_start = time.time()

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(extract_text, url) for url in lista_limpia]
    lista_texto_total = [future.result() for future in futures]

print("With threads time:", time.time() - without_threads_start)