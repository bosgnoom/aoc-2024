import pytest
from opdracht_1b import *


@pytest.fixture
def get_sample_data():
    # Read file input
    a, b = import_file('1/example_a.txt')

    return a, b


@pytest.fixture
def get_left_row(get_sample_data):
    a, b = get_sample_data
    return a


@pytest.fixture
def get_right_row(get_sample_data):
    a, b = get_sample_data
    return b


def test_1(get_right_row):
    # The first number in the left list is 3. It appears
    # in the right list three times, so the similarity
    # score increases by 3 * 3 = 9.
    assert calc_similarity([3], get_right_row) == 9


def test_2(get_right_row):
    # The second number in the left list is 4. It appears
    # in the right list once, so the similarity score
    # increases by 4 * 1 = 4.
    assert calc_similarity([4], get_right_row) == 4


def test_3(get_right_row):
    # The third number in the left list is 2. It does not
    # appear in the right list, so the similarity score
    # does not increase (2 * 0 = 0).
    assert calc_similarity([2], get_right_row) == 0


def test_4(get_right_row):
    # The fourth number, 1, also does not appear in the right list.
    assert calc_similarity([1], get_right_row) == 0


def test_5(get_right_row):
    # The fifth number, 3, appears in the right list
    # three times; the similarity score increases by 9.
    assert calc_similarity([3], get_right_row) == 9


def test_6(get_right_row):
    # The last number, 3, appears in the right list three
    # times; the similarity score again increases by 9.
    assert calc_similarity([3], get_right_row) == 9


def test_opdracht_1b(get_sample_data):
    # Read file input
    a, b = get_sample_data

    # Calculate similarity score
    sim = calc_similarity(a, b)

    assert sim == 31
