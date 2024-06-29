#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    int toascii(int c);
    string text = get_string("Text: ");
    int letters = 0;
    int sentences = 0;
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (toascii(text[i]) >= 65 && toascii(text[i]) <= 122)
        {
            letters++;
        }
        if ((text[i] == '.' || text[i] == '?' || text[i] == '!'))
        {
            sentences++;
        }
        else if (text[i] == ' ' && toascii(text[i + 1]) >= 65 && toascii(text[i + 1]) <= 122)
        {
            words++;
        }
    }
    float L = ((float) letters / (float) words) * 100;
    float S = ((float) sentences / (float) words) * 100;
    float x = (0.0588 * ((float) L));
    float y = (0.296 * ((float) S));
    double readability = (float) x - (float) y - 15.8;
    if (readability > 16)
    {
        printf("Grade 16+\n");
    }
    else if (readability < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %.0f\n", readability);
    }
}