"""
Needs: special order

X|Y: X needs to be before Y

Given:
- ordering rules
- pages to produce

Question A: Which updates are already in the right order?
Question B: Fix those not in order
"""


def read_puzzle(filename: str) -> list:
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


def check_sequence(page, ordering):

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


def fix_sequence(page, ordering):
    #

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


ordering, b = read_puzzle('5/input.txt')

results_correct = []
results_incorrect = []
for page in b:
    print(f'Pages: {page}', end='')
    if check_sequence(page, ordering):
        results_correct.append(page[len(page) // 2])
    else:
        fixed = fix_sequence(page, ordering)
        results_incorrect.append(fixed[len(fixed) // 2])
    print()

print(f'Opdracht 5A: {sum(results_correct)}')  # 7307
# 123 in example, 4713 in input
print(f'Opdracht 5B: {sum(results_incorrect)}')

# page = '75,97,47,61,53'
# page = '61,13,29'
# page = '97,13,75,29,47'
# page = [int(p) for p in page.split(',')]

# print(page)
# print(fix_sequence(page, ordering))
