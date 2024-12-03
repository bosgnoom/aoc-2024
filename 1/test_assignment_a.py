from opdracht_1a import import_file, calc_differences


def test_1():
    # The smallest number in the left list is 1,
    # and the smallest number in the right list is 3.
    # The distance between them is 2.
    assert calc_differences([1], [3]) == [2]


def test_2():
    # The second-smallest number in the left list is 2,
    # and the second-smallest number in the right list is
    # another 3. The distance between them is 1.
    assert calc_differences([2], [3]) == [1]


def test_3():
    # The third-smallest number in both lists is 3,
    # so the distance between them is 0.
    assert calc_differences([3], [3]) == [0]


def test_4():
    # The next numbers to pair up are 3 and 4,
    # a distance of 1.
    assert calc_differences([3], [4]) == [1]


def test_5():
    # The fifth-smallest numbers in each list are
    # 3 and 5, a distance of 2.
    assert calc_differences([3], [5]) == [2]


def test_6():
    # Finally, the largest number in the left list is 4,
    # while the largest number in the right list is 9;
    # these are a distance 5 apart.
    assert calc_differences([4], [9]) == [5]


def test_example():
    a, b = import_file('1/example_a.txt')
    test_diffs = calc_differences(a, b)
    print(test_diffs)
    assert sum(test_diffs) == 11
