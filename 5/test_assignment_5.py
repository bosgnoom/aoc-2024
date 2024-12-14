import pytest

from opdracht_5 import main


def test_opdracht_5():
    assert main('5/example.txt') == (143, 123)


retcode = pytest.main(['-vv', '5/'])
