import pandas as pd
import requests

#Extract the text of the relevant parts of the paper that is in JSON format (title, abstract, introduction, and conclusion) using DataFrames.
#IN:
#   API_URL: URL with the paper in JSON format.
#OUT:
#   text: A list of the extracted text.

def extract_text(API_URL):
    text = []
    json_response = requests.get(API_URL).json()
    df1 = pd.json_normalize(json_response, max_level=1)
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