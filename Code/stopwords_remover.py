import os
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Input the directories')
parser.add_argument('-s', '--stopwords_path', type = str, help = 'enter the stop words folder directory')
parser.add_argument('-e', '--extracted_text_path', type = str, help = 'enter extracted text folder directory')
parser.add_argument('-d','--destination', help = 'enter the path where filtered text will be stored')

args = parser.parse_args()
stopwords_path = args.stopwords_path
extracted_text_path = args.extracted_text_path
dest = args.destination

# collecting all stop words in a temporary single text file: allstopwords.txt

temp_file_path = stopwords_path + '/allwords.txt'

with open(temp_file_path, 'w', encoding = 'latin-1') as outfile:
  print('----Storing all stopwords file in a single file----\n')
  for filename in tqdm(os.listdir(stopwords_path), desc = 'Loading'):
    f = os.path.join(stopwords_path, filename)
    if os.path.isfile(f):
      # encoded with latin-1 to read all the texts
      with open(f, 'r', encoding = 'latin-1') as infile:
        outfile.write(str(infile.read().split()))

# making a list of all stop words

stopwords = []
with open(temp_file_path, 'r', encoding = 'latin-1') as words:
  stopwords = words.read()
#print(stopwords)

# deleting the allstopwords.txt

os.remove(temp_file_path)

# filtering the extracted data from the given stop words
# and saving the filtered files in filtered data folder

print('\n----Filtering the extracted files----\n')

for filename in tqdm(os.listdir(extracted_text_path), desc = 'Loading'):
  f = os.path.join(extracted_text_path, filename)
  if os.path.isfile(f):
    with open(f, 'r') as file1:
      #print(filename)
      words = file1.read().split()
      path_filtered = dest + '/filtered_' + filename
      try:
        appendfile = open(path_filtered, 'r+')
        appendfile.truncate(0)
        appendfile.close()
      except:
        pass
      appendfile = open(path_filtered, 'a')
      for r in words:
        if not r in stopwords:
          appendfile.write(r + ' ')
      appendfile.close()

print('\n----Text files are filtered and stored at {}----'.format(dest))