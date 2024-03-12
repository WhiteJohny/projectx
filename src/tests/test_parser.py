from src.parser.parser import parser


def test_parser_example():
    assert parser(1) == "Yes"
