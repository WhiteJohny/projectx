from src.parser.parsers.for_bot.fox_search import fox_search
from src.parser.parsers.for_bot.fox_result import fox_result
from src.model.model import model_imitation


def fox_many_parser(search_query):
    news_list = []

    links = fox_search(search_query)

    for link in links:
        news_list.append(fox_result(link))

    return model_imitation(news_list)


def fox_one_parser(url):
    text = fox_result(url)

    if text is None:
        return "Ваша ссылка недействительна или она не с foxnews"

    return "Это позитивная новость!" if model_imitation([text])[:3] == '100' else "Это печальная новость("
