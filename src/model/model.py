from random import randint


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
