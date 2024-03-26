from src.parser.parsers.ready.nn_parser import nn_many_parser, nn_one_parser


def test_nn_many_parser():
    assert nn_many_parser("Putin")[1] in list(map(str, [i for i in range(10)]))


def test_nn_one_parser():
    valid_url = "https://www.newsinlevels.com/products/princess-of-wales-has-cancer-level-1/"
    invalid_url1 = ("https://www.foxbusiness.com/industrials/ex-merchant-marine-captain-warns-no-way-controlling-cargo"
                    "-ship-mechanical-error")
    invalid_url2 = "qwerty"

    assert nn_one_parser(valid_url) in ["Это позитивная новость!", "Это печальная новость("]
    assert nn_one_parser(invalid_url1) == "Ваша ссылка недействительна или она не с nn"
    assert nn_one_parser(invalid_url2) == "Ваша ссылка недействительна или она не с nn"
