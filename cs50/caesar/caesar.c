// Project description can be found at: https://cs50.harvard.edu/x/2023/psets/2/caesar/

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string encrypt(string text, int key);
bool isnum(string text);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (isnum(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (atoi(argv[1]) > 0)
    {
        string plaintext = get_string("plaintext:  ");
        printf("ciphertext: %s\n", encrypt(plaintext, atoi(argv[1])));
    }
}

string encrypt(string text, int key)
{
    for (int i = 0; i < strlen(text); i++)
    {
        for (int j = 0; j < key; j++)
        {
            text[i]++;
            if (isalpha(text[i]) == false)
            {
                text[i] -= 1;
                if (isalpha(text[i]) && isupper(text[i]))
                {
                    text[i] = 'A';
                }
                else if (isalpha(text[i]) && islower(text[i]))
                {
                    text[i] = 'a';
                }
            }
        }
    }
    return text;
}

bool isnum(string text)
{
    int n = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isdigit(text[i]) == false)
        {
            n++;
        }
    }
    if (n > 0)
    {
        return false;
    }
    else
    {
        return true;
    }
}
