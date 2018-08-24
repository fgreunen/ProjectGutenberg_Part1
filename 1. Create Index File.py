import os
import glob
from os.path import basename, splitext

INDEX_FILE = u'C:/Users/bbdnet1601/Desktop/Copy Over/ProjectGutenberg/Output/index.txt'
DATA_DIR = u'C:/Users/bbdnet1601/Desktop/Copy Over/ProjectGutenberg/Data/**/*.ZIP'

def get_identifier(x):
    filename = splitext(basename(x))[0]
    underscoreIndex = filename.find('_') >= 0
    if (underscoreIndex >= 0):
        return filename[:underscoreIndex]
    return filename

allFiles = glob.glob(DATA_DIR, recursive = True)
allFiles = [x for x in allFiles if splitext(basename(x))[0].find('_H') < 0 and splitext(basename(x))[0].find('_M') < 0]

identifiers = []
files = []
for x in [x for x in allFiles if splitext(basename(x))[0].find('_') < 0]:
    files.append(x)
    identifiers.append(get_identifier(x))
for x in [x for x in allFiles if splitext(basename(x))[0].find('_') >= 0]:
    if (not get_identifier(x) in identifiers):
        files.append(x)
        identifiers.append(get_identifier(x))

with open(INDEX_FILE, 'w') as f: 
    for file in files:
        f.write("%s\n" % file)
print("Created index file with %s entries." % len(files))