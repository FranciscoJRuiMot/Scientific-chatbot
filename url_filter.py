import requests

#Apply a filter for functional URLs
#IN:
#   url: The URL that is going to be filtered.
#   filtered_urls_list: A list with the functional URLs filtered
#OUT:
#   filtered_urls_list: The updated list.

def url_filter (url, filtered_urls_list):
    response = requests.get(url)
    if response.ok and response.text.lower().split()[:5] != ['no', 'record', 'can', 'be', 'found']:
        filtered_urls_list.append(url)
    return filtered_urls_list