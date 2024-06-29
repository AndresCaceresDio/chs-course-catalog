#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool isletters(string text);
string encrypt(string text, string key);
int toascii(int c);
bool duplicates(string text);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (isletters(argv[1]) == false)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (duplicates(argv[1]) == true)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        string plaintext = get_string("plaintext:  ");
        printf("ciphertext: %s\n", encrypt(plaintext, argv[1]));
    }
}

bool isletters(string text)
{
    int n = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]) == false)
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

string encrypt(string text, string key)
{
    int x = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        x = 0;
        if (islower(text[i]))
        {
            int n = toascii(text[i]);
            for (int j = 97; j < n; j++)
            {
                x++;
            }
            text[i] = tolower(key[x]);
            printf("%i\n", x);
            x = 0;
        }
        else if (isupper(text[i]))
        {
            int n = toascii(text[i]);
            for (int j = 65; j < n; j++)
            {
                x++;
            }
            text[i] = toupper(key[x]);
            printf("%i\n", x);
            x = 0;
        }
        x = 0;
    }
    return text;
}

bool duplicates(string text)
{
    int n = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        for (int j = strlen(text); j != i; j--)
        {
            if (text[i] == text[j])
            {
                n++;
            }
        }
    }
    if (n != 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}