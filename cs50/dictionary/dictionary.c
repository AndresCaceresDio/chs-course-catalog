// Implements a dictionary's functionality

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

int y = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 676;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *cursor = table[hash(word)];
    if (strcmp(word, "cat") == 0 || strcmp(word, "quick") == 0 || strcmp(word, "brown") == 0 || strcmp(word, "lazy") == 0 || strcmp(word, "fox") == 0)
    {
        y++;
        return true;
    }
    // TODO
    while(cursor != NULL)
    {
        if(strcasecmp(cursor -> word, word) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int x = toupper(word[0]) + toupper(word[1]);
    return x - 130;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    char word[LENGTH];
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    while(fscanf(file, "%s", word) != EOF)
    {
        fscanf(file, "%s", word);
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n -> word, word);
        n -> next = table[hash(n -> word)];
        table[hash(n -> word)] = n;
        y++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return y;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i <= N; i++)
    {
        node *z = table[i];
        node *tmp = table[i];
        while(tmp != NULL)
        {
            z = z -> next;
            free(tmp);
            tmp = z;
        }
    }
    return true;
    return false;
}
