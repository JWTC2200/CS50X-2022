#include <cs50.h>
#include <stdio.h>

int main(void)

{
    int n;

    //ask for user input
    do
    {
        n = get_int("width: ");
    }
    //ignore anything not 1-8
    while (n < 1 || n > 8);

    //number of times to run/rows
    //rows = r
    for (int r = 0; r < n; r++)
    {
        //first half
        //spaces = s
        //no. of spaces is input minus rows so spaces reduce as rows loop counts up
        for (int s = n - r; s > 1; s--)
        {
            printf(" ");
        }
        //hash = h insert hash
        //only prints # up to the row number
        for (int h = 0; h <= r; h++)
        {
            printf("#");
        }
        //middle spaces
        //unsure if this needs to be a variable?
        printf("  ");
        //second half
        //reverse first half copied over
        //h for hash insert hash
        for (int h = 0; h <= r; h++)
        {
            printf("#");
        }
        //move to next line
        printf("\n");
    }
}

// ask user for number of steps
// create number of steps specified by user 1-8
//ignore not 1-8
//create # two sides based on "steps"