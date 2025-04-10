"""Module for interactive terminal queries"""

import json
from typing import Callable

from pyquaca import Query


def interactive(
    query_type: Callable[..., Query],
    needs_api_key: bool = False,
    needs_lang: bool = False,
) -> None:
    """Terminal Interface queries"""
    api_key = None
    if needs_api_key:
        api_key = input("Enter your API key: ")
        while not api_key or len(api_key) == 0:
            api_key = input("Please enter a valid API key: ")

    lang = None
    if needs_lang:
        lang = input("Enter the language (default: 'fr'): ")
        if not lang or len(lang) == 0:
            lang = "fr"

    if needs_api_key and needs_lang:
        query = query_type(lang=lang, api_key=api_key)
    elif needs_lang:
        query = query_type(lang=lang)
    elif needs_api_key:
        query = query_type(api_key=api_key)
    else:
        query = query_type()

    while True:
        search_string = input("Enter the search string (or 'exit' to quit): ")
        if search_string.lower() == "exit":
            break
        result = query.query(search_string)
        if result:
            print(json.dumps(result, indent=4))
        else:
            print("No results found.")
