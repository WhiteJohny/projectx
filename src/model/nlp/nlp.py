import numpy as np
import pandas as pd
import json
import string
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from clearml import Dataset
import os
nltk.download('stopwords')
nltk.download('wordnet')


def remove_punctuations(text):
    return "".join([char for char in text if char not in string.punctuation])


def tokenise(text):
    return re.split(r"\W+", text)


def remove_stopwords(text):
    stopword = nltk.corpus.stopwords.words("english")
    return [word for word in text if word not in stopword]


def lemmatizing(text):
    w = nltk.WordNetLemmatizer()
    return " ".join([w.lemmatize(word) for word in text])


def processing_dataset(raw_dataset_id: str, vector_size: int = 0):
    print("Загрузка датасета для обработки...")
    raw_dataset = Dataset.get(dataset_id=raw_dataset_id)
    data = pd.read_csv(raw_dataset.get_local_copy() + "/dataset.csv")

    print("Обработка датасета...")
    data["text"] = data["Sentence"]
    data["sentiment"] = data["Sentiment"]
    data = data.drop(["Sentence", "Sentiment"], axis=1)
    s0 = data[data["sentiment"] == 0]
    s1 = data[data["sentiment"] == 1]
    le = 50000
    data = pd.concat([s1[0 - le // 2:], s0[0 - le // 2:]])
    data["text"] = data['text'].apply(lambda x: remove_punctuations(x))
    data["text"] = data['text'].apply(lambda x: tokenise(x.lower()))
    data["text"] = data['text'].apply(lambda x: remove_stopwords(x))
    data["text"] = data['text'].apply(lambda x: lemmatizing(x))

    # векторизация
    cv = CountVectorizer()
    d = cv.fit_transform(data["text"])
    d = d.toarray()
    labels = list(cv.vocabulary_.keys())
    labels = dict((word, index) for index, word in enumerate(labels))

    # обрезка
    df = pd.DataFrame(d, data['sentiment'])
    sorted_df = df.loc[:, df.sum().sort_values().index]
    column_names = sorted_df.columns.tolist()
    processed_data = sorted_df[column_names[0 - vector_size:]]
    labels = {k: labels[k] for k in labels if labels[k] in processed_data.columns.tolist()}
    b = 0
    for i in labels:
        labels[i] = b
        b += 1
    print("Сохранение датасета...")
    tags = ["labeled", "preprocessed"]
    if vector_size > 0: tags.append("reduced")
    processed_dataset = Dataset.create(
        dataset_name=raw_dataset.name,
        dataset_project=raw_dataset.project,
        parent_datasets=[raw_dataset],
        dataset_tags=tags
    )
    processed_dataset.set_metadata({
        'input_size': vector_size,
        'output_size': 1,
    })
    processed_data.to_csv("dataset.csv")
    with open("labels.json", "w") as f:
        json.dump(labels, f)
    processed_dataset.add_files("dataset.csv")
    processed_dataset.add_files("labels.json")
    processed_dataset.upload()
    processed_dataset.finalize()
    os.remove("dataset.csv")
    os.remove("labels.json")

    print("Готово")
    return processed_data


def processing_string(x, labels):
    x = remove_punctuations(x)
    x = tokenise(x.lower())
    x = remove_stopwords(x)
    x = lemmatizing(x)

    # векторизация
    f = np.zeros(len(labels))
    for i in x.split():
        if i in labels:
            f[labels[i]] += 1

    return f
