import pytest

from opgave_15a import main_a
from opgave_15b import main_b


def test_example_a_1():
    assert main_a('15/ex1.txt', SHOW=False) == 2028


def test_example_a_2():
    assert main_a('15/ex2.txt', SHOW=False) == 10092


def test_assignment_15a():
    assert main_a('15/input.txt', SHOW=False) == 1526673


def test_example_b_1():
    assert main_b('15/ex2.txt', SHOW=False) == 9021


def test_assignment_15b():
    assert main_b('15/input.txt', SHOW=False) == 1535509


# Via this pytest can run via "run"
retcode = pytest.main(['-vv', '15/'])
