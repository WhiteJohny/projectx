from src.model.model import model_imitation


def test_model_imitation():
    assert model_imitation([None, None]) == "Новостей по такому ключевому слову(ам) нет"
    assert model_imitation(['text'])[:3] in ["0% ", "100"]
