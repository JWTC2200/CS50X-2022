#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //get input from user
    string text = get_string("input here: \n");

    int let = count_letters(text);
    int word = count_words(text);
    int sent = count_sentences(text);

    //get average number of words and convert into float
    float w = word / 100.0;
    float l = let / w;
    float s = sent / w;

    //apply CL formula
    int index = round((0.0588 * l) - (0.296 * s) - 15.8);

    //print results
    //below 1
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    // >16
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    // everything else
    else
    {
        printf("Grade %i\n", index);
    }
}
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters += 1;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 1 ;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 32)
        {
            words += 1;
        }
    }
    return words;
}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] ==  33) || (text[i] ==  46) || (text[i] ==  63))
        {
            sentences += 1;
        }
    }
    return sentences;
}