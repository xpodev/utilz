from typing import TypeVar, Callable

_T = TypeVar("_T")


def find_index(items: list[_T], item_key: int, key: Callable[[_T], int]) -> int:
    start, end = 0, len(items)

    while start != end and (end - start) != 1:
        idx = (start + end) // 2
        candidate_key = key(items[idx])
        if item_key < candidate_key:
            end = idx
        elif item_key > candidate_key:
            start = idx
        else:
            return item_key
    else:
        return end
