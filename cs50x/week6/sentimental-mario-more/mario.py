# TODO

from cs50 import get_int


def main():
    height = get_height()
    spaces = height
    for i in range(height):
        print(" " * (height - 1), end="")
        print("#" * (spaces + 1 - height), end="")
        print("  ", end="")
        print("#" * (spaces + 1 - height), end="")
        height -= 1
        print("")


def get_height():
    while True:
        height = get_int("Height please: ")
        if height > 0 and height < 9:
            break
    return height


main()