from src.model.model import Model


MODEL_NAME = "News Sentiment Model"


# инициализация модели
model = Model(model_name=MODEL_NAME)


def get_news_sentiment_one(text):
    sentiment = model.get_news_sentiment(text)
    if sentiment <= 0.4: return "Это печальная новость("
    if sentiment < 0.6: return "Не могу определить, хорошая или плохая новость :/"
    return "Это позитивная новость!"


def get_news_sentiment_many(texts):
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
