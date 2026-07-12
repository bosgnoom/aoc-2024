# ex1.txt --> 7036
# ex2.txt --> 11048
#

import pytest

from assignment_16a import part_a
from assignment_16b import part_b


def test_example_a_1():
    assert part_a('16/ex1.txt', SHOW=False) == 7036


def test_example_a_2():
    assert part_a('16/ex2.txt', SHOW=False) == 11048


def test_example_b_1():
    assert part_b('16/ex1.txt', SHOW=False) == 45


def test_example_b_2():
    assert part_b('16/ex2.txt', SHOW=False) == 64


# Via this pytest can run via "run"
retcode = pytest.main(['-vv', '16/'])
