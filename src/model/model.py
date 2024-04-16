import warnings
import clearml
from src.model.neural_networks import CustomNN
from src.model.nlp import processing_string
from random import randint


PROJECT_NAME = "ProjectX"
MIN_RECOGNIZED_WORDS = 10


def model_imitation(news_list):
    if not news_list or news_list == [None, None]:
        return "Новостей по такому ключевому слову(ам) нет"

    good_mood = counter = 0

    for news in news_list:
        if news is None:
            continue

        counter += 1
        if randint(0, 1):
            good_mood += 1

    return f'{round((good_mood / (counter or 1)) * 100)}% позитивных новостей на данной неделе!'


class Model:
    def __init__(self, model_id: str = None, model_name: str = None):
        """
        Load model based on name or id. Either one or the other must be specified
        :param model_id: Model ID. If specified, ``model_name`` is ignored
        :param model_name: Model name to query. The latest model with this name will be used
        """
        if model_id is not None:
            model = clearml.Model(model_id)
        elif model_name is not None:
            model = clearml.Model.query_models(project_name=PROJECT_NAME, model_name=model_name, max_results=1)[0]
        else:
            raise ValueError("model name or id must be specified")
        self.network = CustomNN.from_file(model.get_weights())
        self.labels = model.labels

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
