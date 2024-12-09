import pytest

from opdracht_8a import read_puzzle, find_antennae, find_coords, find_antinodes, find_antinodes_2


@pytest.fixture
def ex1():
    return read_puzzle('8/ex1.txt')


@pytest.fixture
def ex2():
    return read_puzzle('8/ex2.txt')


@pytest.fixture
def ex3():
    return read_puzzle('8/ex3.txt')


@pytest.fixture
def example():
    return read_puzzle('8/example.txt')


@pytest.fixture
def coords_ex1(ex1):
    return find_coords(ex1, 'a')


@pytest.fixture
def coords_ex2(ex2):
    return find_coords(ex2, 'a')


@pytest.fixture
def coords_ex3(ex3):
    return find_coords(ex3, 'a')


def test_find_ants_1(ex1):
    assert find_antennae(ex1) == ['a']


def test_find_coords_1(ex1):
    assert find_coords(ex1, 'a') == [(3, 4), (5, 5)]


def test_find_ants_1(ex1, coords_ex1):
    assert set(find_antinodes(ex1, coords_ex1)) == set([(1, 3), (7, 6)])


def test_find_ants_2(ex2, coords_ex2):
    assert set(find_antinodes(ex2, coords_ex2)) == set(
        [(2, 0), (1, 3), (7, 6), (6, 2)])


def test_find_ants_3(ex3, coords_ex3):
    assert set(find_antinodes(ex3, coords_ex3)) == set(
        [(2, 0), (1, 3), (7, 6), (6, 2)])


def test_find_example(example):
    total = []

    for a in find_antennae(example):

        coords = find_coords(example, a)
        result = find_antinodes(example, coords)
        total += result

    assert len(set(total)) == 14


def test_find_example_2_ex5():
    example = read_puzzle('8/ex5.txt')

    total = []

    for a in find_antennae(example):

        coords = find_coords(example, a)
        result = find_antinodes_2(example, coords)
        total += result

    assert len(set(total)) == 9


def test_find_example_2_full(example):
    total = []

    for a in find_antennae(example):

        coords = find_coords(example, a)
        result = find_antinodes_2(example, coords)
        total += result

    assert len(set(total)) == 34


retcode = pytest.main(['-vv', '8/'])
