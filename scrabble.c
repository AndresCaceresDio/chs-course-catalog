#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int n = 0;

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    //Checks which word had a higher score and prints the winner or prints a tie
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else if (score1 == score2)
    {
        printf("Tie!\n");
    }

}

int compute_score(string word)
{
    n = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        //Checks  the letter of the inputted word and adds its according valueto the variable n
        if (tolower(word[i]) == 'a' || tolower(word[i]) == 'e' || tolower(word[i]) == 'i' || tolower(word[i]) == 'l'
            || tolower(word[i]) == 'n' || tolower(word[i]) == 'o' || tolower(word[i]) == 'r' || tolower(word[i]) == 's'
            || tolower(word[i]) == 't' || tolower(word[i]) == 'u')
        {
            n++;
        }
        else if (tolower(word[i]) == 'd' || tolower(word[i]) == 'g')
        {
            n += 2;
        }
        else if (tolower(word[i]) == 'b' || tolower(word[i]) == 'c' || tolower(word[i]) == 'm' || tolower(word[i]) == 'p')
        {
            n += 3;
        }
        else if (tolower(word[i]) == 'f' || tolower(word[i]) == 'h' || tolower(word[i]) == 'v' || tolower(word[i]) == 'w'
                 || tolower(word[i]) == 'y')
        {
            n += 4;
        }
        else if (tolower(word[i]) == 'k')
        {
            n += 5;
        }
        else if (tolower(word[i]) == 'j' || tolower(word[i]) == 'x')
        {
            n += 8;
        }
        else if (tolower(word[i]) == 'q' || tolower(word[i]) == 'z')
        {
            n += 10;
        }
    }
    //Returns the total value of the inputted word
    return n;
}
