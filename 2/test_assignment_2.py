from opdracht_2a import opdracht_a, check_differences, calc_differences
from opdracht_2b import opdracht_b, check_differences_damperer


def test_a1():
    # 7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
    assert check_differences(calc_differences([7, 6, 4, 2, 1]))


def test_a2():
    # 1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
    assert not check_differences(calc_differences([1, 2, 7, 8, 9]))


def test_a3():
    # 9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
    assert not check_differences(calc_differences([9, 7, 6, 2, 1]))


def test_a4():
    # 1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
    assert not check_differences(calc_differences([1, 3, 2, 4, 5]))


def test_a5():
    # 8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
    assert not check_differences(calc_differences([8, 6, 4, 4, 1]))


def test_a6():
    # 1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
    assert check_differences(calc_differences([1, 3, 6, 7, 9]))


def test_a_example():
    assert opdracht_a('2/example.txt') == 2


def test_b1():
    # 7 6 4 2 1: Safe without removing any level.
    assert check_differences_damperer([7, 6, 4, 2, 1])


def test_b2():
    # 1 2 7 8 9: Unsafe regardless of which level is removed.
    assert not check_differences_damperer([1, 2, 7, 8, 9])


def test_b3():
    # 9 7 6 2 1: Unsafe regardless of which level is removed.
    assert not check_differences_damperer([9, 7, 6, 2, 1])


def test_b4():
    # 1 3 2 4 5: Safe by removing the second level, 3.
    assert check_differences_damperer([1, 3, 2, 4, 5])


def test_b5():
    # 8 6 4 4 1: Safe by removing the third level, 4.
    assert check_differences_damperer([8, 6, 4, 4, 1])


def test_b6():
    # 1 3 6 7 9: Safe without removing any level.
    assert check_differences_damperer([1, 3, 6, 7, 9])


def test_b_example():
    assert opdracht_b('2/example.txt') == 4
