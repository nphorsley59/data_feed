from typing import List


def build_search_string(keywords: List[str] | str, oa: bool = True) -> str:
    if isinstance(keywords, str):
        search_string = keywords
    elif isinstance(keywords, list):
        search_string = " AND ".join(keywords)
    else:
        raise ValueError(f"Invalid type for keywords: {type(keywords)}")
    if oa:
        search_string = f"{search_string} AND open access[filter]"
    return search_string


def format_number_with_commas(number: int) -> str:
    return f"{number:,}"
