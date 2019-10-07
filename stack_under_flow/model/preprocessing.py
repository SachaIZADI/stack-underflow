# TODO:
"""

- Beautiful soup to parse HTML replace <code/> by $CODE$
- Html2Text
- expand contractions
- nltk extract sentences
- Train embeddings: https://blog.cambridgespark.com/tutorial-build-your-own-embedding-and-use-it-in-a-neural-network-e9cde4a81296
"""


# https://pastebin.com/YsCTpeQB








# Define a stopwords dictionnary :

stopwords = nltk.corpus.stopwords.words('english')

# We keep the negative adverbs
stopwords.remove('no')
stopwords.remove('not')

# We remove the iphone and galaxy vocabulary
stopwords.append('iphone')
stopwords.append('apple')
stopwords.append('samsung')
stopwords.append('galaxy')
stopwords.append('s8')

print(stopwords)


 We want to keep the negative indicators (e.g. wouldn't --> keep not).
# So we need to expand common English contractions
# To do so, we use a bit of code from StackOverFlow



# this code is not mine! i shamelessly copied it from http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
# all credits go to alko and arturomp @ stack overflow.
# basically, it's a big find/replace.

cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text.lower())

# examples
print (expandContractions('Don\'t you get it?'))
print (expandContractions('I ain\'t got time for y\'alls foolishness'))
print (expandContractions('You won\'t live to see tomorrow.'))
print (expandContractions('You\'ve got serious cojones coming in here like that.'))
print (expandContractions('I hadn\'t\'ve enough'))


def preprocessing(string):
    string = str(string)
    # lower_case
    string = string.lower()
    # remove accents
    string = unidecode.unidecode(string)
    # expand English contractions
    string = expandContractions(string)
    # remove stopwords
    pattern = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')
    string = pattern.sub('', string)
    # remove special caracters like "" and punctuation
    string = re.sub('[^A-Za-z0-9 ]','', string)
    # lematize
    string = nltk.stem.wordnet.WordNetLemmatizer().lemmatize(string,"v")
    string = nltk.stem.wordnet.WordNetLemmatizer().lemmatize(string,"a")
    string = nltk.stem.wordnet.WordNetLemmatizer().lemmatize(string)
    return(string)

TFIDF_train = TfidfVectorizer(
    input='content',
    lowercase=False,
    preprocessor=preprocessing
)

# https://scikit-learn.org/stable/modules/compose.html