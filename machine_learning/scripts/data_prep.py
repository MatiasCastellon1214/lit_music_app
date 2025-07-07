import pandas as pd
import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def load_data(path= "../data/merged_reviews.csv"):
    
    df = pd.read_csv(path)
    df = df[df['review/score'] != 3]
    df['label'] = df['review/score'].apply(lambda x: 1 if x > 3 else 0)

    return df


def clean_text(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower().split()
    text = [lemmatizer.lemmatize(word) for word in text if word not in set(stopwords.words('english')) and len(word) > 2]
    return ' '.join(text)


def prepare_corpus(df, column, limit=None):
    corpus = []
    limit = limit if limit else len(df)
    for i in range(limit):
        corpus.append(clean_text(df[column][i]))
    return corpus