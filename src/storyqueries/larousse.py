"""Larousse Query Class"""

# type: ignore[unused-ignore]
import os
import unicodedata
from typing import Any, no_type_check

import bs4
from pyquaca import JSONCache, Parser, Query, QueryConfig
from requests import Response

from storyqueries import interactive


class LarousseParser(Parser):
    """Parse the response from Larousse"""

    def parse_grammar(self, soup: bs4.BeautifulSoup) -> str | None:
        """Parse the grammar from Larousse"""
        grammar: str = ""
        try:
            grammar = soup(class_="CatgramDefinition")[0].find(  # type: ignore
                string=True, recursive=False
            )
        except IndexError:
            return None
        return grammar

    def parse_word(self, soup: bs4.BeautifulSoup) -> str | None:
        """Parse the word from Larousse"""
        try:
            word = None
            for text_part in soup(class_="AdresseDefinition"):
                for content in text_part.contents:  # type: ignore
                    if not isinstance(content, bs4.element.NavigableString):
                        continue
                    if len("".join(e for e in content if e.isalnum())) < 1:
                        continue
                    word = str(content)
                    break
            if word and "," in word:
                word = word.split(",", maxsplit=1)[0]
            self.logger.info("using base form: %s", word)
        except IndexError:
            word = None
        return word

    def parse_definitions(self, soup: bs4.BeautifulSoup) -> list[dict[str, str]]:
        """Parse definitions from Larousse"""
        formatted_definitions = []
        try:
            definitions = soup.select(".Definitions .DivisionDefinition")
            for definition in definitions:
                definition_text = "".join(
                    [
                        text
                        for text in definition.contents
                        if isinstance(text, bs4.element.NavigableString)
                    ]
                )
                normalized_text = unicodedata.normalize("NFKD", definition_text.strip())
                formatted_definitions.append({"definition": normalized_text})
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error("Error parsing definitions: %s", e)
        return formatted_definitions

    def parse_expressions(self, soup: bs4.BeautifulSoup) -> list[dict[str, str]]:
        """Parse the expressions from Larousse"""
        expressions = []
        try:
            locutions = soup.find_all(class_="Locution")
            for x in locutions:
                express = {}
                text = x.find(class_="AdresseLocution").find(  # type: ignore
                    string=True, recursive=False
                )
                definition = x.find(class_="TexteLocution").text  # type: ignore
                express["expression"] = text.strip(", ")
                express["definition"] = definition
                expressions.append(express)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error("Error parsing expressions: %s", e)
        return expressions

    def parse_warnings(self, soup: bs4.BeautifulSoup) -> list[str]:
        """Parse the warnings from Larousse"""
        warnings = []
        try:
            for d in soup.find_all(class_="DefinitionDifficulte"):
                warnings.append(d.text.replace("\xa0", " "))
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error("Error parsing difficulties: %s", e)
        return warnings

    def parse_citations(self, soup: bs4.BeautifulSoup) -> list[dict[str, str]]:
        """Parse citations from Larousse"""
        citations = []

        def find(cell: Any, x: str) -> str | Any:
            return cell.find(class_=x).text

        try:
            for c in soup.find_all(class_="ListeCitations"):
                c_dict = {}
                try:
                    c_dict["Author"] = find(c, "AuteurCitation")
                except Exception:  # pylint: disable=broad-except
                    c_dict["Author"] = ""
                try:
                    c_dict["Info"] = find(c, "InfoAuteurCitation")
                except Exception:  # pylint: disable=broad-except
                    c_dict["Info"] = ""
                try:
                    c_dict["Text"] = find(c, "TexteCitation")
                except Exception:  # pylint: disable=broad-except
                    c_dict["Text"] = ""
                try:
                    c_dict["Reference"] = find(c, "ReferenceCitation")
                except Exception:  # pylint: disable=broad-except
                    c_dict["Reference"] = ""
                citations.append(c_dict)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error("Error parsing citations: %s", e)
        return citations

    @no_type_check
    def parse(self, raw: Response) -> dict:
        """Parse the raw data from Larousse"""
        soup = bs4.BeautifulSoup(raw.text, "html.parser")
        word = self.parse_word(soup)
        grammar = self.parse_grammar(soup)
        definitions = self.parse_definitions(soup)
        expressions = self.parse_expressions(soup)
        warnings = self.parse_warnings(soup)
        citations = self.parse_citations(soup)

        return {
            "word": word,
            "grammar": grammar,
            "definitions": definitions,
            "expressions": expressions,
            "warnings": warnings,
            "citations": citations,
        }


class QueryLarousse(Query):  # pylint: disable=too-few-public-methods
    """Query Configured to send queries to Larousse"""

    def __init__(self, check_cache: bool = True, cache_path: str = "cache") -> None:
        cache = JSONCache(os.path.join(cache_path, "larousse"))
        config: QueryConfig = {
            "check_cache": check_cache,
            "parser": LarousseParser(),
            "cache": cache,
        }
        url = "https://www.larousse.fr/dictionnaires/francais/{search_string}/"
        super().__init__(url, config)


if __name__ == "__main__":
    interactive.interactive(QueryLarousse)
