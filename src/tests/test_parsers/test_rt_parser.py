from src.parser.parsers.ready.rt_parser import rt_many_parser, rt_one_parser


def test_rt_many_parser():
    assert rt_many_parser("Trump")


def test_rt_one_parser():
    valid_url = "https://www.rt.com/business/594932-russia-oil-north-korea-sanctions/"
    invalid_url1 = ("https://www.foxbusiness.com/industrials/ex-merchant-marine-captain-warns-no-way-controlling-cargo"
                    "-ship-mechanical-error")
    invalid_url2 = "qwerty"

    assert rt_one_parser(valid_url) is str
    assert rt_one_parser(invalid_url1) is None
    assert rt_one_parser(invalid_url2) is None
