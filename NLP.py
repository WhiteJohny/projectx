import pandas as pd
import string
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer


def remove_punctuations(text):
    return "".join([char for char in text if char not in string.punctuation])


def tokenise(text):
    return re.split("\W+", text)


def remove_stopwords(text):
    stopword = nltk.corpus.stopwords.words("english")
    return [word for word in text if word not in stopword]


def lemmatizing(text):
    w = nltk.WordNetLemmatizer()
    return " ".join([w.lemmatize(word) for word in text])


def vectorization(text):
    cv = CountVectorizer()
    d = cv.fit_transform(text)
    d = d.toarray()
    return d


def processing_dataset(s):
    data = pd.read_csv("Sentiment_dataset.csv")
    data = data.drop(["news_title", "reddit_title", "url"], axis=1)
    data["text"] = data['text'].apply(lambda x: remove_punctuations(x))
    data["text"] = data['text'].apply(lambda x: tokenise(x.lower()))
    data["text"] = data['text'].apply(lambda x: remove_stopwords(x))
    data["text"] = data['text'].apply(lambda x: lemmatizing(x))
    d = vectorization(data["text"])
    df = pd.DataFrame(d, data['sentiment'])
    sorted_df = df.loc[:, df.sum().sort_values().index]
    column_names = sorted_df.columns.tolist()
    return sorted_df[column_names[0 - s:]]

def processing_string(x):
    x = remove_punctuations(x)
    x = tokenise(x.lower())
    x = remove_stopwords(x)
    x = lemmatizing(x)
    return x

s = 100
a = "adams For example, annex 38 regulates the requirements pertaining to wastewater from textile manufacturing and textile finishing plants."
g = processing_dataset(s)
h = processing_string(a)
print(h)
print(g)
