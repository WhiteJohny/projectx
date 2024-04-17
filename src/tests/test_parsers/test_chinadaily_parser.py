from src.parser.parsers.ready.chinadaily_parser import chinadaily_many_parser, chinadaily_one_parser


def test_chinadaily_many_parser():
    assert chinadaily_many_parser("Trump")


def test_chinadaily_one_parser():
    valid_url = "https://www.chinadaily.com.cn/a/202404/14/WS661b292ea31082fc043c1d25.html"
    invalid_url1 = ("https://www.foxbusiness.com/industrials/ex-merchant-marine-captain-warns-no-way-controlling-cargo"
                    "-ship-mechanical-error")
    invalid_url2 = "qwerty"

    assert type(chinadaily_one_parser(valid_url)) == str
    assert chinadaily_one_parser(invalid_url1) is None
    assert chinadaily_one_parser(invalid_url2) is None
