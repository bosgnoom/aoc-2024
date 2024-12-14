import pytest

from opdracht_9a import main


def test_9a():
    assert main('9/example.txt') == 1928


retcode = pytest.main(['-vv', '9/'])
