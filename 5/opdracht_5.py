"""
Needs: special order

X|Y: X needs to be before Y

Given:
- ordering rules
- pages to produce

Question A: Which updates are already in the right order?
Question B: Fix those not in order
"""


def read_puzzle(filename: str) -> tuple[list, list]:
    """Reads puzzle, both parts

    Args:
        filename (str): filename

    Returns:
        tuple[list,list]: order of pages and list of pages to be sorted
    """
    with open(filename) as f:
        lines = f.readlines()

    section_switch = True

    order = []
    pages = []
    for line in lines:
        line = line.strip('\n')

        if line == '':
            section_switch = False
        elif section_switch:
            order.append(line)
        else:
            pages.append([int(ll) for ll in line.split(',')])

    ordering = []
    for o in order:
        left = o.split('|')[0]
        right = o.split('|')[1]
        ordering.append([int(left), int(right)])

    return ordering, pages


def check_sequence(page: list, ordering: list[list]) -> bool:
    """Checks if sequence of pages is in order

    Args:
        page (list): list of page numbers
        ordering (list[list]): ordering of the pages

    Returns:
        bool: checks are all OK
    """

    for order in ordering:
        # check positions in page
        if (order[0] in page) and (order[1] in page):
            left = page.index(order[0])
            right = page.index(order[1])
            if (left < right):
                # print("      ", order, "ok")
                print('.', end='')
                pass
            else:
                # print("      ", order, "not ok")
                return False

    return True


def fix_sequence(page: list, ordering: list[list]) -> list:
    """Fix order of pages,

    Do this by flipping positions of pages which are out of order

    Args:
        page (list): Input pages (book)
        ordering (list[list]): Needed order

    Returns:
        list: Reshuffled pages
    """

    for order in ordering:
        # check whether the order items are in the given pages
        if (order[0] in page) and (order[1] in page):
            left = page.index(order[0])
            right = page.index(order[1])
            if (left < right):
                # print("      ", order, "ok")
                pass
            else:
                # print("      ", order, "not ok")
                print('.', end='')
                # Let's try to swap positions of these
                page[left], page[right] = page[right], page[left]

                return fix_sequence(page, ordering)

    return page


def main(filename: str):
    """Runs assignment 5 for both part a and b

    Args:
        filename (str): Puzzle input

    Returns:
        tuple: puzzle output
    """
    ordering, books = read_puzzle(filename)

    results_correct = []
    results_incorrect = []

    # Loop over all input
    for page in books:
        print(f'Pages: {page}', end='')
        if check_sequence(page, ordering):
            results_correct.append(page[len(page) // 2])
        else:
            fixed = fix_sequence(page, ordering)
            results_incorrect.append(fixed[len(fixed) // 2])
        print('\n')

    # 143 in example, 7307
    print(f'Opdracht 5A: {sum(results_correct)}')

    # 123 in example, 4713 in input
    print(f'Opdracht 5B: {sum(results_incorrect)}')

    return sum(results_correct), sum(results_incorrect)


if __name__ == "__main__":
    assert main('5/input.txt') == (7307, 4713)
