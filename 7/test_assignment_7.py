import pytest

from opdracht_7 import read_puzzle, calculate_row, main


def test_7a_1():
    assert calculate_row([190, 10, 19]) == 190


def test_7a_2():
    assert calculate_row([3267, 81, 40, 27]) == 3267


def test_7a_3():
    assert calculate_row([292, 11, 6, 16, 20]) == 292


def test_7a_example():
    assert main('7/example.txt') == 3749


def test_7b_1():
    assert calculate_row([156, 15, 6], operations='*+|') == 156


def test_7b_2():
    assert calculate_row([7290, 6, 8, 6, 15], operations='*+|') == 7290


def test_7b_3():
    assert calculate_row([192, 17, 8, 14], operations='*+|') == 192


def test_7b_example():
    assert main('7/example.txt', operations='*+|') == 11387
