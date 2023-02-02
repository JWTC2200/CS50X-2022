from cs50 import get_int, get_string
from math import ceil


def main():
    card_no = get_card_no()
    validate = odds(card_no) + evens(card_no)
    # validate first then check individual card conditions
    if validate % 10 != 0:
        print("INVALID")
    else:
        first = int(card_no[0])
        second = int(card_no[1])
        length = len(card_no)

        if first == 3 and (second == 4 or second == 7):
            print("AMEX")
        elif first == 5 and (1 <= second <= 5):
            print("MASTERCARD")
        elif first == 4 and (length == 13 or length == 16):
            print("VISA")
        else:
            print("INVALID")

# ask for card number, prompt again if invalid


def get_card_no():
    while True:
        try:
            card_no = get_string("No: ")
            if int(card_no) > 0:
                break
        except ValueError:
            print("Try again")
    return card_no


# calculate all odd numbers
def odds(card_no):
    length = len(card_no)
    inter = 1
    sum = 0
    # use ceil to round up
    # treat card number as array and convert individual numbers to sum
    for i in range(ceil(length/2)):
        inter -= 2
        sum += int(card_no[inter])
    return sum


# calculate all even numbers
def evens(card_no):
    length = len(card_no)
    inter = 0
    even_string = ""
    for i in range(int(length/2)):
        inter -= 2
        # multiply by 2 then add to string in case answer is 2 digit, i.e. 10, 12 , 14 or 16
        even_string += str(int(card_no[inter]) * 2)
    # reset inter to use again
    inter = 0
    sum = 0
    # convert string into numbers and get sum
    for i in range(len(even_string)):
        inter -= 1
        sum += int(even_string[inter])
    return sum


main()