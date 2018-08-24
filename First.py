from mrjob.job import MRJob
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import ToktokTokenizer
from nltk.corpus import stopwords
from collections import Counter
import time

# cd C:/Users/bbdnet1601/Desktop/MR
# python First.py Data/*.txt > result
 
tokenizer = ToktokTokenizer()
all_stopwords = set(stopwords.words('english')) | set(['\\n', '``', '\'\'', '--', '\'s', '\'\'i', '\'ve', '\'ll', '\'i', '\'m',  'gutenberg-tm', 'n\'t'])
filters = [ lambda x: len(x) > 1, 
            lambda x: not x.isnumeric(), 
            lambda x: not x in all_stopwords]

def timerfunc(func):
    def function_timer(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "The runtime for {func} took {time} seconds to complete"
        print(msg.format(func=func.__name__, time=runtime))
        return value
    return function_timer

def nFilter(filters, tuples):
    for f in filters:
        tuples = filter(f, tuples)
    return tuples

def get_word_counts_from_raw(raw):
    return get_word_counts(raw.split('\n'))

def get_word_counts(lines):
    startIndex = [i for i, s in enumerate(lines) if '*** START OF THIS PROJECT GUTENBERG EBOOK' in s][0] + 1
    endIndex = [i for i, s in enumerate(lines) if '*** END OF THIS PROJECT GUTENBERG EBOOK' in s][0] - 1
    return Counter([word for word in 
        nFilter(filters, 
            tokenizer.tokenize(
                    (' '.join(lines[startIndex:endIndex]))
                        .lower()
                        .replace('\n', '')
                )
            )]).most_common() # sort it

@timerfunc
def do_thing():
    file = u'C:/Users/bbdnet1601/Desktop/Copy Over/ProjectGutenberg/Output/Extracted/11.txt'
    with open(file, 'r') as f:
        raw = f.read()
    counts = get_word_counts_from_raw(raw)
    for word, frequency in counts[:10]:
        print(u'{} - {}'.format(word, frequency))

class MRJobName(MRJob):
    def mapper(self, _, file):
        yield 'WORD', len(file)
        # counts = get_word_counts_from_raw(file)
        # for word, frequency in counts:
            # yield word, frequency

    def reducer(self, word, counts):
        i,totalL,totalW=0,0,0
        for i in counts:
            totalL += 1
            totalW += i     
        yield "AVG", totalW/float(totalL)


if __name__ == '__main__':
    do_thing()
    # MRJobName.run()