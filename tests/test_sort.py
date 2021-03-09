from log_processing_demo import sort


def test_sort_list_of_digits() -> None:
    my_list = [2, 1, 5, 4, 3]
    sorted_list = [1, 2, 3, 4, 5]
    sort.sort(my_list)
    assert my_list == sorted_list


def test_sort_corner_cases() -> None:
    empty_list = []
    one_element_list = [1]
    two_element_list = [2, 1]
    duplicate_element_list = [1, 2, 1]

    sort.sort(empty_list)
    sort.sort(one_element_list)
    sort.sort(two_element_list)
    sort.sort(duplicate_element_list)

    assert empty_list == []
    assert one_element_list == [1]
    assert two_element_list == [1, 2]
    assert duplicate_element_list == [1, 1, 2]


def test_sort_real_data(fake_log_list, fake_log_list_sorted):
    def key(element):
        return element["created_at"]

    my_list = fake_log_list
    sort.sort(my_list, key=key)
    assert my_list == fake_log_list_sorted
