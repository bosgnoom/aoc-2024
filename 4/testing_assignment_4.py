import pytest
from opdracht_4a import read_puzzle, count_word_occurrences
from opdracht_4b import opdracht_4b


@pytest.fixture
def read_example():
    return read_puzzle('4/example.txt')


def test_a(read_example):
    assert count_word_occurrences(read_example, 'XMAS') == 18


def test_b(read_example):
    assert opdracht_4b(read_example) == 9
