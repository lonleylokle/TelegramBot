import unittest
from Bot import *
from parserKassir import *


class MyTestCase(unittest.TestCase):
    def test_send_product(self):
        self.assertIsNotNone(send_product(123))

    def test_parse_cities(self):
        self.assertIsNone(parse_cities())

    def test_parser_search(self):
        self.assertIsNotNone(parser_search("text"))

    def test_search_product(self):
        test = {"message_id": 2494,
                "from": {"id": 221468810, "is_bot": "false",
                         "first_name": "Тест", "username": "Test",
                         "language_code": "en"},
                "chat": {"id": 221468810, "first_name": "Тест",
                         "username": "Test", "type": "private"},
                "date": 1587588361,
                "text": "test"}
        self.assertIsNotNone(search_product(test))


if __name__ == '__main__':
    unittest.main()
