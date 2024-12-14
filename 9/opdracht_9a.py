# This one is so dirty...

def main(filename):
    with open(filename) as f:
        disk = f.readline().strip('\n')

    # First examples in text
    # disk = '12345'
    # disk = '2333133121414131402'

    # Alternating file-free space

    # 12345 --> 0..111....22222 -->
    # 0..111....22222
    # 02.111....2222.
    # 022111....222..
    # 0221112...22...
    # 02211122..2....
    # 022111222......

    # 2333133121414131402 --> 00...111...2...333.44.5555.6666.777.888899

    # Developing...
    printing = len(disk) < 25
    disk_ids = []

    current_id = 0
    # Fill disk (this will be bad I guess for numbers > 9)
    for id, d in enumerate(disk):
        if id % 2 == 0:
            # Even ones (indexing starts at zero!) --> File
            disk_ids += ([current_id] * int(d))
            current_id += 1
        else:
            # Odd ones --> Empty space
            disk_ids += ([None] * int(d))

    if printing:
        print(disk_ids)

    def get_last_id(a):
        for i, e in enumerate(reversed(a)):
            if e is not None:
                return len(a) - i - 1
        return None

    def print_disk(disk_ids):
        if printing:
            for x in disk_ids:
                if x is not None:
                    print(x, end='')
                else:
                    print('.', end='')
            print()

    # Defragment disk
    if printing:
        print_disk(disk_ids)

    for id, d in enumerate(disk_ids):
        # id = index of disk
        # d  = item on disk (id or .)

        if d is None:
            # Empty spot, fill with last file id

            # Find where last file is (position in list)
            last_file_pos = get_last_id(disk_ids)

            # Find out what file it is (the id of the file)
            last_file_id = disk_ids[last_file_pos]

            # Stop when defrag is complete
            if last_file_pos < id:
                print('\nStopping here!')
                break

            # Update disk
            disk_ids[id] = last_file_id
            disk_ids[last_file_pos] = None

            # Show progress
            if printing:
                print_disk(disk_ids)

        # Show progress during full input
        if (id % 1000 == 0) and not printing:
            print('.', end='')

    # Now calculate checksum
    checksum = 0
    for id, x in enumerate(disk_ids):
        if x is not None:
            checksum += id * disk_ids[id]

    print(f'\nChecksum: {checksum}')   # 6370402949053

    return checksum


if __name__ == "__main__":
    # main('9/example.txt')
    main('9/input.txt')
