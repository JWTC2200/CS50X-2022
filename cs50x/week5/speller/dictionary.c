// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include "dictionary.h"
#define _GNU_SOURCE
#include <strings.h>


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//counter for size function
int counter = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //hash word
    unsigned int location = hash(word);
    //go to table[hashresult]
    node *cursor = table[location];
    //loop check strcmp cursor target with word else move on. stop if null
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function

    int sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        if (isalpha(word[i]))
        {
            sum = sum + (toupper(word[i]) - 'A') * strlen(word);
        }
    }
    return sum;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //open file
    // then for every word string run a loop? recursively add words into hash table.
    FILE *tocheck = fopen(dictionary, "r");
    if (tocheck == NULL)
    {
        return false;
    }
    // for (some loop)
    char buffer[LENGTH + 1];

    while (fscanf(tocheck, "%s", buffer) != EOF)
    {
        // node for strcopy
        node *load = malloc(sizeof(node));
        if (load == NULL)
        {
            return false;
        }
        //copy
        strcpy(load->word, buffer);
        load->next = NULL;
        // hashnumber in list
        unsigned int hashno = hash(load->word);
        //insert word
        if (table[hashno] != NULL)
        {
            load->next = table[hashno];
        }
        else
        {
            load->next = NULL;
        }
        table[hashno] = load;

        //increase counter size
        counter++;
    }
    fclose(tocheck);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    //cursor and temp
    // cursor = cursor->next
    // free tmp
    // tmp = cursor

    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = NULL;
        while (cursor != NULL)
        {
            tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }

    }
    return true;
}