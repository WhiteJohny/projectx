from src.parser.parsers.ready.rt_parser import rt_many_parser, rt_one_parser


def test_rt_many_parser():
    assert rt_many_parser("Trump")[1] in list(map(str, [i for i in range(10)]))


def test_rt_one_parser():
    valid_url = "https://www.rt.com/business/594932-russia-oil-north-korea-sanctions/"
    invalid_url1 = ("https://www.foxbusiness.com/industrials/ex-merchant-marine-captain-warns-no-way-controlling-cargo"
                    "-ship-mechanical-error")
    invalid_url2 = "qwerty"

    assert rt_one_parser(valid_url) in ["Это позитивная новость!", "Это печальная новость("]
    assert rt_one_parser(invalid_url1) == "Ваша ссылка недействительна или она не с rt"
    assert rt_one_parser(invalid_url2) == "Ваша ссылка недействительна или она не с rt"
