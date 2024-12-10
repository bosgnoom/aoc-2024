# Broken...
# Nog iets erbij zetten of de file al verplaatst is
import time


def get_last_id(a):
    for i, e in enumerate(reversed(a)):
        if e is not None:
            return len(a) - i - 1
    return None


def get_last_pos(a, pos):
    look_for = None
    file_length = 0
    b = a[0:pos]
    for i, e in enumerate(reversed(b)):
        if e is not None and look_for is None:
            look_for = e
            # print(f'looking for: {e}')
        if look_for is not None:
            if e == look_for:
                file_length += 1
            else:
                return (len(b) - i, file_length)
    print('kak')
    exit(-1)
    return (None, None)


def print_disk(disk_ids):
    if printing:
        for x in disk_ids:
            if x is not None:
                print(x, end='')
            else:
                print('.', end='')
        print()


# Read input
with open('9/input.txt') as f:
    disk = f.readline().strip('\n')

# First examples in text
disk = '2333133121414131402'

# When developing...
printing = len(disk) < 25

# Fill disk, as a list with filenumbers
current_id = 0
disk_ids = []

for id, d in enumerate(disk):
    if id % 2 == 0:
        # Even ones (indexing starts at zero!) --> File
        disk_ids += ([current_id] * int(d))
        current_id += 1
    else:
        # Odd ones --> Empty space
        disk_ids += ([None] * int(d))


# Defragment disk
if printing:
    print_disk(disk_ids)

# Set starting positions
id = 0
last_pos = len(disk_ids)
last_file, file_size = get_last_pos(disk_ids, last_pos)

while True:
    # id = index of disk
    # d  = item on disk (id or .)
    d = disk_ids[id]

    # Show what we're doing
    filename = ''.join([str(x)
                       for x in disk_ids[last_file:last_file+file_size]])
    print(f'Looking for a spot for file {filename} at {id=}')

    # Find an empty spot
    if d is None:
        print(f'at {id=}')
        # Empty spot, find out how large it is,
        fragment = 0

        while True:
            item = disk_ids[id + fragment]

            if item is not None:
                break

            fragment += 1

        print(f'Size of fragment: {fragment}')

        # Check if file fits inside fragment
        if fragment >= file_size:
            print('Fits, moving file...')
            disk_ids[id:id+file_size] = disk_ids[last_file:last_file+file_size]
            disk_ids[last_file:last_file+file_size] = [None] * file_size

            # File has been moved, reset defrag
            id = 0
            last_pos = last_file

            # Find last file and size
            last_file, file_size = get_last_pos(disk_ids, last_pos)
            print(f'{last_file=}, {file_size=}, file: ')
        else:
            print('Does not fit, skipping position...')
            id += fragment

        if id >= last_file:
            print('Reached file position, skipping file!')
            id = 0
            last_pos = last_file

            # Find last file and size
            last_file, file_size = get_last_pos(disk_ids, last_pos)
            print(f'{last_file=}, {file_size=}, file: ')

        print()

        # Show progress
        if printing:
            print_disk(disk_ids)
    else:
        # Not an empty space, next position
        id += 1

    # Show progress during full input
    if (id % 1000 == 0) and not printing:
        print('.', end='')

    # end of loop

# Now calculate checksum 2858
checksum = 0
for id, x in enumerate(disk_ids):
    if x is not None:
        checksum += id * disk_ids[id]

print(f'\nChecksum: {checksum}')   # 6370402949053 for A, 6398096697992 for B
