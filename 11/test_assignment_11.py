import pytest

from opdracht_11a import main
from opdracht_11b import main_b, read_puzzle


def test_11a():
    assert main() == 199753


def test_11b():
    puzzle = read_puzzle('5 62914 65 972 0 805922 6521 1639064')
    length, stones = main_b(puzzle, 25)  # 199753
    assert length == 199753


retcode = pytest.main(['-vv', '11/'])
