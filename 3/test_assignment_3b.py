from opdracht_3b import process_memory


def test_sample():
    line = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    assert process_memory(line) == 48
