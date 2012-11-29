"""

  The main function. Assume all characters are in ASCII.

"""

import sys, random

from url import URL

def get_strings(f):
  strings = []
  line = f.readline()
  while len(line) > 0:
    # do not add empty line
    if len(line) > 1:
      strings.append(line[:len(line) - 1])
    line = f.readline()
  return strings

if __name__ == "__main__":

  filename = None
  if len(sys.argv) != 3:
    print 'Usage: python validator.py input-file output-file'
    exit(1)

  inputfile = open(sys.argv[1])

  strings = get_strings(inputfile)
  urls = [URL(x) for x in strings]
  unique_original_urls = {}
  unique_normalized_urls = {}
  
  for url in urls:
    if url.url in unique_original_urls:
      unique_original_urls[url.url] = False
    else:
      unique_original_urls[url.url] = True

    if url.getNormalized() in unique_normalized_urls:
      unique_normalized_urls[url.getNormalized()] = False
    else:
      unique_normalized_urls[url.getNormalized()] = True

  outputfile = open(sys.argv[2], 'w+')

  for url in urls:
    original_url = url.url
    is_valid = str(url.isValid())
    canonical = url.getNormalized()
    source_unique = str(unique_original_urls[url.url])
    canonical_unique = str(unique_normalized_urls[url.getNormalized()])

    outputfile.write('Source: ' + original_url + '\n')
    outputfile.write('Valid: ' + is_valid + '\n')
    outputfile.write('Canonical: ' + canonical + '\n')
    outputfile.write('Source unique: ' + source_unique + '\n')
    outputfile.write('Cannonicalized URL unique: ' + canonical_unique + '\n\n')

  inputfile.close()
  outputfile.close()
