from __future__ import annotations
import warnings
import clearml
from src.model.neural_networks import *
from src.model.nlp import processing_string


PROJECT_NAME = "ProjectX"
MODEL_NAME = "News Sentiment Model"
MIN_RECOGNIZED_WORDS = 10


class Model:
    def __init__(self, model_id: str = None, model_name: str = None):
        """
        Load model based on name or id. Either one or the other must be specified
        :param model_id: Model ID. If specified, ``model_name`` is ignored
        :param model_name: Model name to query. The latest model with this name will be used
        """
        if model_id is not None:
            print(f"Загрузка модели {model_id}...")
            model = clearml.Model(model_id)
        elif model_name is not None:
            print(f"Загрузка модели {model_name}...")
            model = clearml.Model.query_models(project_name=PROJECT_NAME, model_name=model_name, max_results=1)[0]
        else:
            raise ValueError("model name or id must be specified")
        self.labels = model.labels
        try:
            framework = FRAMEWORKS[model.framework]
            self.network = framework.from_file(model.get_weights())
        except KeyError:
            raise NotImplementedError(f"{model.framework} framework not implemented")
        print(f"Модель {model.name} загружена (ID: {model.id})")

    def get_news_sentiment(self, news_text: str) -> float:
        """
        Get the sentiment of a news article using the model
        :param news_text: The text of the news article
        :return: Float representing sentiment in the range of 0 (bad sentiment) to 1 (good sentiment)
        """
        processed_text = processing_string(news_text, self.labels)
        if processed_text.sum() < MIN_RECOGNIZED_WORDS:
            warnings.warn("model could not recognize enough words in given text", RuntimeWarning)
            return 0.5
        return self.network.eval(processed_text)[0]


# инициализация
model = Model(model_name=MODEL_NAME)


def get_news_sentiment_one(text: str) -> str:
    if model is None: raise RuntimeError("model not initialized")
    if text is None: return "Ваша ссылка недействительна"
    sentiment = model.get_news_sentiment(text)
    if sentiment <= 0.4: return "Это печальная новость("
    if sentiment < 0.6: return "Не могу определить, хорошая или плохая новость :/"
    return "Это позитивная новость!"


def get_news_sentiment_many(texts: list[str]) -> str:
    if model is None: raise RuntimeError("model not initialized")
    sentiments = [model.get_news_sentiment(text) for text in texts]

    if sentiments:
        good_sentiments = 0.0
        for sentiment in sentiments:
            if sentiment >= 0.6: good_sentiments += 1
            elif sentiment > 0.4: good_sentiments += 0.5
        percentage = round((good_sentiments / len(sentiments)) * 100)
    else:
        percentage = 0
    return f"{percentage}% позитивных новостей!"
