"""Test the Lexicala API"""

import unittest
from unittest import mock

from storyqueries.lexicala import QueryLexicala

parsed_data = {
    "n_results": 1,
    "page_number": 1,
    "results_per_page": 10,
    "n_pages": 1,
    "available_n_pages": 1,
    "results": [
        {
            "id": "FR_DE8a05953e8fe9",
            "language": "fr",
            "headword": {"text": "poire", "pos": "noun"},
            "senses": [{"id": "FR_SEe33a8061df64", "definition": "fruit"}],
        }
    ],
    "word": "poire",
}


class Test(unittest.TestCase):
    """Test the Lexicala API"""

    def test_query_lexicala(self):
        """Test the Lexicala query"""
        ql = QueryLexicala(check_cache=False)
        ql.requester = mock.Mock()
        ql.requester.request = mock.Mock()
        ql.requester.request.return_value = parsed_data
        ql.parser = mock.Mock()
        ql.parser.parse = mock.Mock()
        ql.parser.parse.return_value = parsed_data
        data = ql.query("poire")
        self.assertNotEqual(data, None)
        print(data)
        results = data.get("results")
        self.assertNotEqual(results, None)
        self.assertEqual(len(results), 1)
        senses = results[0].get("senses")
        self.assertEqual(len(senses), 1)
        self.assertIsNotNone(senses[0].get("definition"))


if __name__ == "__main__":
    unittest.main()
