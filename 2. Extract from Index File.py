import zipfile
import os
import glob
from os.path import basename, splitext
import shutil

INDEX_FILE = u'C:/Users/bbdnet1601/Desktop/Copy Over/ProjectGutenberg/Output/index.txt'
DATA_DIR = u'C:/Users/bbdnet1601/Desktop/Copy Over/ProjectGutenberg/Output/Extracted'

def step1_unzip():
    if (os.path.exists(DATA_DIR)): 
        shutil.rmtree(DATA_DIR)
    shown = set([])
    files = [file.rstrip('\n') for file in open(INDEX_FILE)]
    for index, file in enumerate(files):
        zip_ref = zipfile.ZipFile(file, 'r')
        zip_ref.extractall(DATA_DIR)
        zip_ref.close()
        progress = int(100 * index / len(files))
        if (progress % 5 == 0 and not progress in shown):
            print(progress)
            shown.add(progress)

def step2_clean_directories():
    # clean out the directories
    dirs = [f.path for f in os.scandir(DATA_DIR) if f.is_dir() ]   
    for d in dirs:
        for file in glob.glob(d + "/*.txt"):
            new = DATA_DIR + '/' + basename(file)
            shutil.move(file, os.path.join(DATA_DIR, basename(file)))
        shutil.rmtree(d)

def step3_remove_non_text():
    # remove all non-txt files
    for f in os.listdir(DATA_DIR):
        if (not f.lower().endswith(".txt")):
            os.remove(os.path.join(DATA_DIR, f))

def step4_remove_non_english():
    for f in os.listdir(DATA_DIR):
        try:
            if (not 'Language: English' in open(os.path.join(DATA_DIR, f)).read()):
                os.remove(os.path.join(DATA_DIR, f))
        except:
            os.remove(os.path.join(DATA_DIR, f))

def step5_create_without_headers():
    counter = 0
    for f in os.listdir(DATA_DIR):
        counter += 1
        with open(os.path.join(DATA_DIR, f), 'r') as file:
            lines = file.readlines()

        startIndex = [i for i, s in enumerate(lines) if '*** START OF THIS PROJECT GUTENBERG EBOOK' in s]
        endIndex = [i for i, s in enumerate(lines) if '*** END OF THIS PROJECT GUTENBERG EBOOK' in s]
        if (len(startIndex) > 0 and len(endIndex) > 0):
            startIndex = startIndex[0] + 1
            endIndex = endIndex[0] - 1
            raw = ' '.join(lines[startIndex:endIndex])
            newFilename = os.path.join(DATA_DIR, 'raw.' + f)
            with open(newFilename, 'w') as file:
                file.write(raw)
        os.remove(os.path.join(DATA_DIR, f))
        if (counter % 100 == 0):
            print(counter)

# step1_unzip()
# step2_clean_directories()
# step3_remove_non_text()
# step4_remove_non_english()
step5_create_without_headers()