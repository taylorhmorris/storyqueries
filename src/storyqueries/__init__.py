"""StoryQueries: a Python module to query language data."""

from .interactive import interactive
from .larousse import QueryLarousse
from .lexicala import QueryLexicala
from .linguee import QueryLinguee
from .pixabay import QueryPixabay

__all__ = (
    "QueryPixabay",
    "QueryLarousse",
    "QueryLexicala",
    "QueryLinguee",
    "QueryHFLLM",
    "QueryHFTTI",
    "interactive",
)
