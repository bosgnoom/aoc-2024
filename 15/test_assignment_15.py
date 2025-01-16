import pytest

from opgave_15a import main


def test_example1():
    assert main('15/ex1.txt', SHOW=False) == 2028


def test_example2():
    assert main('15/ex2.txt', SHOW=False) == 10092


def test_assignment_15a():
    assert main('15/input.txt', SHOW=False) == 1526673


# Via this pytest can run via "run"
retcode = pytest.main(['-vv', '15/'])
