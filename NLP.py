import pandas as pd
import json
import string
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from clearml import Dataset
import os


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


def vectorization(text):
    cv = CountVectorizer()
    d = cv.fit_transform(text)
    d = d.toarray()
    global labels
    labels = list(cv.vocabulary_.keys())
    labels = dict((index, word) for index, word in enumerate(labels))
    return d


def vectorization_for_str(x: str):
    f = [0] * len(labels)
    for i in x.split():
        try:
            f[l[i]] += 1
        except KeyError:
            pass
    return f


def processing_dataset(raw_dataset_id: str, vector_size: int = 0):
    print("Загрузка датасета для обработки...")
    raw_dataset = Dataset.get(dataset_id=raw_dataset_id)
    data = pd.read_csv(raw_dataset.get_local_copy() + "/dataset.csv")

    print("Обработка датасета...")
    data = data.drop(["news_title", "reddit_title", "url"], axis=1)
    data["text"] = data['text'].apply(lambda x: remove_punctuations(x))
    data["text"] = data['text'].apply(lambda x: tokenise(x.lower()))
    data["text"] = data['text'].apply(lambda x: remove_stopwords(x))
    data["text"] = data['text'].apply(lambda x: lemmatizing(x))
    d = vectorization(data["text"])
    df = pd.DataFrame(d, data['sentiment'])
    sorted_df = df.loc[:, df.sum().sort_values().index]
    column_names = sorted_df.columns.tolist()
    processed_data = sorted_df[column_names[0 - vector_size:]]
    global labels
    labels = {k: labels[k] for k in processed_data.columns.tolist()}
    labels = {labels[k] : k for k in labels}
    b = 0
    for i in l:
        l[i] = b
        b += 1
    with open("labels.json", "w") as f:
        json.dump(labels, f)

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
    processed_dataset.add_files("dataset.csv")
    processed_dataset.add_files("labels.json")
    processed_dataset.upload()
    processed_dataset.finalize()
    os.remove("dataset.csv")
    os.remove("labels.json")

    print("Готово")
    return processed_data


def processing_string(x):
    x = remove_punctuations(x)
    x = tokenise(x.lower())
    x = remove_stopwords(x)
    x = lemmatizing(x)
    return vectorization_for_str(x)


def load_labels():
    with open("labels.json", "r") as f:
        global labels
        labels = json.load(f)


# s = 100
# l = {}
# a = "adams For example, annex 38 regulates the requirements pertaining to wastewater from textile manufacturing and textile finishing plants."
# g = processing_dataset(s)
# p = h.columns.tolist()
# h = processing_string(a)
# print(h)
# print(g)
