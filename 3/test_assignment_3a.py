from opdracht_3a import multiply, analyze_line


def test_multiply():
    assert multiply(44, 46) == 2024
    assert multiply(123, 4) == 492


def test_corrupted_multiply():
    line = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'

    assert analyze_line(line) == 161
