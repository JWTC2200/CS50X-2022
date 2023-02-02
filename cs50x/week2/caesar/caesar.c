#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

bool only_digits(string argxx);
string rotate(string plaint, int);

int main(int argc, string argv[])
{


    //check if code took a single command

    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    //show digits
    string argxx = argv[1];
    //checking the key
    bool onlyd = only_digits(argxx);
    if (onlyd == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //convert argv into int
    int test = atoi(argv[1]);
    //get plaintext input
    string plaint = get_string("plaintext: ");
    string ciphertext = rotate(plaint, test);
    printf("ciphertext: %s\n", ciphertext);
}

//checking the key are only digits
bool only_digits(string argxx)
{
    string s = argxx;
    //set to true, string fails with single non digit
    bool digits = true;
    for (int i = 0; i < strlen(s); i++)
    {
        if (isdigit(s[i]) == false)
        {
            digits = false;
        }
    }
    return digits;
}

// eaiser to keep rotationg as string
string rotate(string plaint, int test)
{
    string cipher = plaint;
    for (int i = 0; i < strlen(plaint); i++)
    {
        //sort by upper lower case
        //adjust by test amount and wrap
        //adjustment for extreme numbers mod26 + adjustment
        if (isupper(plaint[i]))
        {
            cipher[i] = (plaint[i] - 'A' + test) % 26 + 'A';
        }
        else if (islower(plaint[i]))
        {
            cipher[i] = (plaint[i] - 'a' + test) % 26 + 'a';
        }

    }
    return cipher;
}
//