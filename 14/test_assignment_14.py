import pytest

from opgave_14a import main


def test_example():
    assert main('14/ex1.txt', (11, 7)) == 12
