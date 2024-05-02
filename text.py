
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
def extract_text_from_html(html):
    if isinstance(html, str):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text(separator=' ')
            return text
        except Exception as e:
            print(e)
            return html
    else:
        return np.nan
old_file = pd.read_csv(r'mycsv.csv')
old_file['parsed_title'] = old_file['Body (HTML)'].apply(extract_text_from_html)
old_file = old_file.dropna(subset=['parsed_title'])
old_file.to_csv('new.csv', index=False)
print(old_file.head())
