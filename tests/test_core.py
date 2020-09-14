import pytest

from ccb.core import group_items


@pytest.mark.parametrize("items, n, output", [
    ([1, 2, 3], 2, [[1, 2], [3]]),
    ([1, 2, 3], 4, [[1, 2, 3]]),
    ([1, 2, 3, 4], 4, [[1, 2, 3, 4]]),
    ([1, 2, 3, 4, 5], 4, [[1, 2, 3], [4, 5]]),
    ([1, 2, 3, 4, 5, 6], 4, [[1, 2, 3], [4, 5, 6]]),
    ([1, 2, 3, 4, 5, 6, 7], 4, [[1, 2, 3, 4], [5, 6, 7]]),
    ([1, 2, 3, 4, 5, 6, 7, 8], 4, [[1, 2, 3, 4], [5, 6, 7, 8]]),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 4, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
])
def test_group_items(items, n, output):
    assert group_items(items, n) == output
