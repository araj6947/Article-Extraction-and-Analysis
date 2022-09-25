from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib.request, sys, time
import requests
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process some integers')
parser.add_argument('-p', '--path', type = str, help = 'an integer for the accumulator')
parser.add_argument('-d','--destination', help = 'an integer for the accumulator')
args = parser.parse_args()
path = args.path
dest = args.destination
df = pd.read_excel(path)
def gethtmldata(url):
    try:
      page=requests.get(url, headers={"User-Agent": "XY"})
      return page
    except Exception as e:
      error_type, error_obj, error_info = sys.exc_info()
      return error_type, error_obj, error_info

for index, rows in tqdm(df.iterrows(), total = df.shape[0], desc = 'Extracting...'):
    url_id, url = rows['URL_ID'], rows['URL']
    url_id = str(url_id)

    page = gethtmldata(url)

    if page.status_code == 200:
      soup = BeautifulSoup(page.text, 'html.parser')
      try:
        f = soup.find('pre', attrs={'class':'wp-block-preformatted'})
        f.decompose()
      except:
        continue
      data = ''
      destination = dest + url_id + '.txt'
      file1 = open(destination, 'w')
      for data in soup.find_all('div', attrs={'class':'td-post-content'}):
        file1.write(data.get_text())
      file1.close()
    elif page.status_code == 406:
      print('\n406 error at {}'.format(url_id))
      continue
    else:
      print('\nMaybe the site with url_id: {} and url: {} is empty or broken'.format(url_id, url))
      continue

print('\nExtraction done from all the given links and the text files have been saved at {}'.format(dest))
      