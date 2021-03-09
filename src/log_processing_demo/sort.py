"""
Simple in-place Mergesort implementation for training purposes.
Added 'key' function just like in Python STL 'sorted()' to sort arbitrary objects.
"""
from typing import Any, Callable, List, Optional


def sort(input_list: List[Any], key: Optional[Callable[[Any], Any]] = None) -> None:
    """Main wrapper function of the module.

    Parameters
    ----------
    input_list : List[Any]
        List to be sorted.
    key : Optional[Callable[[Any], Any]]
        A function (or other callable) to be called on each list element prior to making comparisons.

    Returns
    -------
    None

    """
    if not input_list:
        return

    _merge_sort(input_list, 0, len(input_list) - 1, key if key else lambda x: x)


def _merge_sort(
    input_list: List[Any],
    left_index: int,
    right_index: int,
    key: Callable[[Any], Any],
) -> None:
    """Merge Sort Recursive Function.

    Parameters
    ----------
    input_list : List[Any]
        List that is being sorted.
    left_index : int
        Left margin of a processing segment.
    right_index : int
        Right margin of a segment.
    key : Callable[[Any], Any]
        Key callable.

    Returns
    -------
    None

    """
    if left_index >= right_index:
        return

    middle: int = (left_index + right_index) // 2

    _merge_sort(input_list, left_index, middle, key)
    _merge_sort(input_list, middle + 1, right_index, key)

    _merge(input_list, left_index, right_index, middle, key)


def _merge(
    input_list: List[Any],
    left_index: int,
    right_index: int,
    middle: int,
    key: Callable[[Any], Any],
) -> None:
    """List merging routine.

    Parameters
    ----------
    input_list : List[Any]
        List that is being sorted.
    left_index : int
        Left margin of a processing segment.
    right_index : int
        Right margin of a segment.
    middle : int
        Middle point of a segment.
    key : Callable[[Any], Any]
        Key callable.

    Returns
    -------
    None

    """
    left_copy: List = input_list[left_index : middle + 1]
    right_copy: List = input_list[middle + 1 : right_index + 1]

    left_copy_index: int = 0
    right_copy_index: int = 0
    sorted_index: int = left_index

    # Merging until one of the halves is exhausted

    while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
        if key(left_copy[left_copy_index]) <= key(right_copy[right_copy_index]):
            input_list[sorted_index] = left_copy[left_copy_index]
            left_copy_index += 1
        else:
            input_list[sorted_index] = right_copy[right_copy_index]
            right_copy_index += 1
        sorted_index += 1

    # Adding the rest

    if left_copy_index < len(left_copy):
        input_list[
            sorted_index : sorted_index + len(left_copy) - left_copy_index
        ] = left_copy[left_copy_index:]

    if right_copy_index < len(right_copy):
        input_list[
            sorted_index : sorted_index + len(right_copy) - right_copy_index
        ] = right_copy[right_copy_index:]
