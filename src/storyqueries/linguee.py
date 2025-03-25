"""Linguee query and parser"""

# pylint: disable=too-few-public-methods
import os
from typing import no_type_check

from bs4 import BeautifulSoup
from pyquaca.json_cache import JSONCache
from pyquaca.parser import Parser
from pyquaca.query import Query, QueryConfig
from requests import Response


class LingueeParser(Parser):
    """Parser for Linguee API response"""

    @no_type_check
    def parse_examples(self, soup: BeautifulSoup) -> list[dict[str, str]]:
        """Parse the examples from Linguee"""
        example_spans = soup.find_all("span", class_="tag_e")
        examples = []
        for span in example_spans:
            source = span.find("span", class_="tag_s").text
            translation = span.find("span", class_="tag_t").text
            examples.append({"source": source, "translation": translation})
        return examples

    @no_type_check
    def parse_expressions(self, soup: BeautifulSoup) -> list[dict[str, str]]:
        """Parse the expressions from Linguee"""
        try:
            expression_group = soup.find_all(class_="example_lines")[-1].text.split(
                "\n\n\n\n"
            )
        except IndexError:
            expression_group = []
        expressions = []
        for expression in expression_group:
            if expression != "":
                pairs = expression.split(":")[-1].strip("\n").split("—")
                if len(pairs) >= 2:
                    expressions.append(
                        {
                            "expression": pairs[0],
                            "translation": pairs[1].replace("\n", ""),
                        }
                    )
        return expressions

    def parse(self, raw: Response) -> dict[str, list[dict[str, str]]]:
        """Parse the data from Linguee"""
        soup = BeautifulSoup(raw.text, "html.parser")
        examples = self.parse_examples(soup)
        expressions = self.parse_expressions(soup)
        results = {"examples": examples, "expressions": expressions}
        return results


class QueryLinguee(Query):
    """Query Configured to send queries to Linguee"""

    def __init__(self, cache_path: str = "cache") -> None:
        url_root = "https://linguee.com/english-french/search"
        url = url_root + "?source=french&query={search_string}"
        parser = LingueeParser()
        cache = JSONCache(os.path.join(cache_path, "linguee"))
        config: QueryConfig = {
            "parser": parser,
            "cache": cache,
        }
        super().__init__(url, config)
