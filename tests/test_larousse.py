"""Test the QueryLarousse class."""

import unittest

from storyqueries.larousse import QueryLarousse


class Test(unittest.TestCase):
    """Test the QueryLarousse class."""

    def test_query_larousse(self):
        """Test the query for "chat" and check if it returns definitions."""
        ql = QueryLarousse(True)
        results = ql.query("chat")
        self.assertEqual(len(results["definitions"]), 8)
        for definition in results["definitions"]:
            self.assertNotRegex(definition["definition"], "^[1-9]")

    def test_query_larousse_expressions(self):
        """Test the query for "chat" and check if it returns expressions."""
        results = QueryLarousse(True).query("chat")
        for expression in results["expressions"]:
            self.assertTrue(expression["expression"][-1] != " ")
            self.assertTrue(expression["expression"][-1] != ",")

    def test_query_larousse_viens_venir(self):
        """Test the query for "viens" and check if it returns "venir" as the word."""
        results = QueryLarousse(True).query("viens")
        self.assertEqual(results.get("word"), "venir")


if __name__ == "__main__":
    unittest.main()
