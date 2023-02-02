#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

bool alphabetical(string key);
bool all_letters(string key);
char substitution(char input, string key);

int main(int argc, string argv[])
{

    //single command check message
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    //command not 26 characters check message
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else
    {
        //check all alphabetical message
        alphabetical(argv[1]);
        //check all 26 letters in key message
        all_letters(argv[1]);

    }
    //key
    string key = argv[1];

    //get plaintext
    printf("plaintext: ");
    string inputtext = get_string("");
    printf("ciphertext: ");
    //print ciphertext
    int i = 0;
    for (i = 0; i < strlen(inputtext);)
    {
        char cipher = substitution(inputtext[i], key);
        printf("%c", cipher);
        i++;
    }
    printf("\n");

}
//check key contains only letters
bool alphabetical(string key)
{
    for (int i = 0; i < strlen(key); i++)
    {
        if (isalpha(key[i]) == 0)
        {
            printf("Key contains non alphabetical characters.\n");
            exit(1);
        }
    }
    return 1;
}
//check key contains one of each letter in alphabet
bool all_letters(string key)
{
    //convert all to same case
    int length = strlen(key);
    int i = 0;
    while (i < length)
    {
        if (islower(key[i]))
        {
            key[i] = toupper(key[i]);
            i++;
        }
        else
        {
            i++;
        }
    }

    //compare results with the rest of the array x != y

    int x = 0;

    while (x < length)
    {
        int y = x + 1;
        while (y < length)
        {
            if (key[x] != key[y])
            {
                y++;
            }
            else
            {
                printf("letterrepeated\n");
                exit(1);
            }
        }
        x++;
    }

    return 1;
}

char substitution(char input, string key)
{
    //use key array as 0-25
    //convert key array to same case
    int length = strlen(key);
    int i = 0;
    while (i < length)
    {
        if (islower(key[i]))
        {
            key[i] = toupper(key[i]);
            i++;
        }
        else
        {
            i++;
        }
    }
    //convert input to same position as key array
    //detect if input is upper or lower adjust value
    //return value
    int result = 0;
    if (isupper(input))
    {
        result = input - 65;
        return key[result];
    }
    else if (islower(input))
    {
        result = input - 97;
        return key[result] + 32;
    }
    else
    {
        return input;
    }
    // key bcd
    // input abC
    // detect ab = lowercase - "a" then compare to key array
    //detect C = uppercase -"A" the compare to array then capitalize
}