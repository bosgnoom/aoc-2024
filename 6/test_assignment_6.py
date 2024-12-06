import pytest

from opdracht_6a import opdracht_6a, read_puzzle, find_elf
from opdracht_6b import opdracht_6b, process_dot


@pytest.fixture
def prep_test_b():
    grid = read_puzzle('6/example.txt')
    pos, dir = find_elf(grid)

    return grid, pos, dir


def test_a_example():
    assert opdracht_6a('6/example.txt') == 41


def test_a_input():
    assert opdracht_6a('6/input.txt') == 5453


def test_b_known_positions_ok(prep_test_b):
    """Test positions in the example grid where from the text
    we know that these will cause an infinite loop
    """
    empty_positions = [(0, 0), (9, 9)]
    grid, pos, dir = prep_test_b
    for dot in empty_positions:
        print(f'Testing dot: {dot}')
        assert process_dot(dot, grid, pos, dir) > 0


def test_b_known_positions_nok(prep_test_b):
    """Test positions in the example grid where from the text
    we know that these will cause an infinite loop
    """
    empty_positions = [(6, 3), (7, 6), (7, 7), (8, 1), (8, 3), (9, 7)]
    grid, pos, dir = prep_test_b
    for dot in empty_positions:
        print(f'Testing dot: {dot}')
        assert process_dot(dot, grid, pos, dir) == 0


def test_b_example():
    assert opdracht_6b('6/example.txt') == 6
