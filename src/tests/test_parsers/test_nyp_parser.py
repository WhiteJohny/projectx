from src.parser.parsers.ready.nyp_parser import nyp_many_parser, nyp_one_parser


def test_nyp_many_parser():
    assert nyp_many_parser("Trump")[1] in list(map(str, [i for i in range(10)]))


def test_nyp_one_parser():
    valid_url = "https://nypost.com/2024/03/26/us-news/robert-f-kennedy-jr-announces-nicole-shanahan-as-vp-pick/"
    invalid_url1 = ("https://www.foxbusiness.com/industrials/ex-merchant-marine-captain-warns-no-way-controlling-cargo"
                    "-ship-mechanical-error")
    invalid_url2 = "qwerty"

    assert nyp_one_parser(valid_url) in ["Это позитивная новость!", "Это печальная новость("]
    assert nyp_one_parser(invalid_url1) == "Ваша ссылка недействительна или она не с nyp"
    assert nyp_one_parser(invalid_url2) == "Ваша ссылка недействительна или она не с nyp"
