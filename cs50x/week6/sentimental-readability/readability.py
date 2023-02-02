from cs50 import get_string


def main():
    text = get_text()
    letters = get_letters(text)
    words = get_words(text)
    sentences = get_sentences(text)
    print(letters, words, sentences)

    # Implement index
    index = round((0.0588 * letters / words * 100) - (0.296 * sentences / words * 100) - 15.8)

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print("Grade", index)


def get_text():
    while True:
        try:
            text = get_string("No: ")
            if len(text) > 0:
                break
        except ValueError:
            print("Try again")
    return text


def get_letters(text):
    letters = 0
    for i in range(len(text)):
        if (text[i].isalpha()):
            letters += 1
    return letters


def get_words(text):
    words = 1
    for i in range(len(text)):
        if (text[i].isspace()):
            words += 1
    return words


def get_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if text[i] == '?' or text[i] == '!' or text[i] == '.':
            sentences += 1
    return sentences


main()