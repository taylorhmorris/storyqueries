"""Lexicala Query Module"""

import json
import os
from typing import no_type_check

import requests
from pyquaca import APIRequester, JSONCache, Parser, Query, QueryConfig


class LexicalaRequester(APIRequester):
    """Requests API data from Lexicala"""

    def __init__(self, url: str, lang: str = "fr", api_key: str = ""):
        super().__init__(url, api_key)
        self.lang = lang
        self.logger = self.logger.getChild("Lexicala")

    def format_url(self, query_string: str) -> str:
        return self.base_url.format(lang=self.lang, search_string=query_string)

    def request(self, query_string: str) -> str | requests.Response | None:
        """Make a request with the given query_string"""
        self.logger.info("Requesting with query_string: %s", query_string)
        url = self.format_url(query_string)
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "lexicala1.p.rapidapi.com",
        }
        response = requests.get(url, timeout=5, headers=headers)
        if response.status_code != 200:
            self.logger.error("Request to %s failed (%s)", url, response.status_code)
            return None
        self.logger.debug("Received response from %s", url)
        return response


class LexicalaParser(Parser):
    """Parse the response from Lexicala"""

    def __init__(self) -> None:
        super().__init__()
        self.logger = self.logger.getChild("Lexicala")

    @no_type_check
    def parse(self, raw: requests.Response) -> dict:
        """Parse the response and return the data"""
        try:
            data = json.loads(raw.content.decode("utf-8"))
            return data
        except Exception as e:
            self.logger.error("Failed to parse response: %s", e)
            return None


class QueryLexicala(Query):
    """Query Configured to send queries to Lexicala"""

    def __init__(
        self,
        lang: str = "fr",
        api_key: str = "",
        cache_path: str = "cache",
        check_cache: bool = True,
    ) -> None:
        url = "https://lexicala1.p.rapidapi.com/search?source=global&language={lang}&text={search_string}"
        self.lang = lang
        cache_path = os.path.join(cache_path, "lexicala")
        config: QueryConfig = {
            "api_key": api_key,
            "requester": LexicalaRequester(url, lang, api_key),
            "parser": LexicalaParser(),
            "cache": JSONCache(cache_path),
            "check_cache": check_cache,
            "cache_path": cache_path,
        }
        super().__init__(url, config)
