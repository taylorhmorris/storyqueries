import logging
import os
import unicodedata

import bs4
from pyquaca import JSONCache, Parser, Query, QueryConfig
from requests import Response


class LarousseParser(Parser):
    def parse(self, raw: Response) -> dict:
        """Parse the raw data from Larousse"""
        soup = bs4.BeautifulSoup(raw.text, "html.parser")
        try:
            word = None
            for text_part in soup(class_="AdresseDefinition"):
                for content in text_part.contents:
                    if not isinstance(content, bs4.element.NavigableString):
                        continue
                    if len("".join(e for e in content if e.isalnum())) < 1:
                        continue
                    word = str(content)
                    break
            if word and "," in word:
                word = word.split(",")[0]
            logging.info(f"Using base form: {word}")
        except IndexError as e:
            word = None
        try:
            grammar = soup(class_="CatgramDefinition")[0].find(
                string=True, recursive=False
            )
        except IndexError:
            grammar = None
        try:
            definitions = soup.select(".Definitions .DivisionDefinition")
            formatted_definitions = []
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

            locutions = soup.find_all(class_="Locution")
            expressions = []
            for x in locutions:
                express = dict()
                expression_text = x.find(class_="AdresseLocution").find(
                    string=True, recursive=False
                )
                expression_defintion = x.find(class_="TexteLocution").text
                express["expression"] = expression_text.strip(", ")
                express["definition"] = expression_defintion
                expressions.append(express)

            difficultes = []
            for d in soup.find_all(class_="DefinitionDifficulte"):
                difficultes.append(d.text.replace("\xa0", " "))

            citations = []
            for c in soup.find_all(class_="ListeCitations"):
                c_dict = {}
                try:
                    c_dict["Author"] = c.find(class_="AuteurCitation").text
                except:
                    c_dict["Author"] = ""
                try:
                    c_dict["Info"] = c.find(class_="InfoAuteurCitation").text
                except:
                    c_dict["Info"] = ""
                try:
                    c_dict["Text"] = c.find(class_="TexteCitation").text
                except:
                    c_dict["Text"] = ""
                try:
                    c_dict["Reference"] = c.find(class_="ReferenceCitation").text
                except:
                    c_dict["Reference"] = ""
                citations.append(c_dict)
            results = {
                "word": word,
                "grammar": grammar,
                "definitions": formatted_definitions,
                "expressions": expressions,
                "warnings": difficultes,
                "citations": citations,
            }
            return results
        except NameError as error:
            logging.error("Name error encountered")
            raise error


class QueryLarousse(Query):
    """Query Configured to send queries to Larousse"""

    def __init__(self, check_cache=True, cache_path="cache"):
        cache = JSONCache(os.path.join(cache_path, "larousse"))
        config: QueryConfig = {
            "check_cache": check_cache,
            "parser": LarousseParser(),
            "cache": cache,
        }
        url = "https://www.larousse.fr/dictionnaires/francais/{search_string}/"
        super().__init__(url, config)
