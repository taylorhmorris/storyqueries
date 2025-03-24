"""Pixabay API Query Class"""

# pylint: disable=too-few-public-methods
import json
import os
from typing import Any

import requests
from query_and_cache.api_requester import APIRequester
from query_and_cache.json_cache import JSONCache
from query_and_cache.parser import Parser
from query_and_cache.query import Query, QueryConfig


class PixabayParser(Parser):
    """Parser for Pixabay API response"""

    def parse(self, raw: requests.Response) -> Any:
        """Parse the data from the Pixabay API"""
        return json.loads(raw.content.decode("utf-8"))


class QueryPixabay(Query):
    """Query Configured to send queries to Pixabay"""

    def __init__(
        self, lang: str = "fr", api_key: str = "", cache_path: str = "cache"
    ) -> None:
        """Initialize the QueryPixabay class"""
        url_root = "https://pixabay.com/api/"
        url_query = "?key={api_key}&q={search_string}&lang={lang}"
        url_extra = "&image_type=photo&safesearch=true"
        url = url_root + url_query + url_extra
        self.lang = lang
        requester = APIRequester(url)
        cache_path = os.path.join(cache_path, "pixabay")
        cache = JSONCache(cache_dir=cache_path)
        parser = PixabayParser()
        config: QueryConfig = {
            "api_key": api_key,
            "requester": requester,
            "cache": cache,
            "parser": parser,
        }
        super().__init__(url, config)
