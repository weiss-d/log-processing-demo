from log_processing_demo import sort


def test_sort_list_of_digits() -> None:
    my_list = [2, 1, 5, 4, 3]
    sorted_list = [1, 2, 3, 4, 5]
    sort.sort(my_list)
    assert my_list == sorted_list
