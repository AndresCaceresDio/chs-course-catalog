#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Gets the height that the user wants the pyramids to be
    int height = 0;
    do
    {
        height = get_int("Height: ");
    }
    while (height > 8 || height < 1);

    int i = 1;

    //Creates the pyramid
    for (int x = 0; x < height; x++)
    {
        //Enters the amount of spaces before each hashtag
        for (int y = (height - 1); y > x; y--)
        {
            printf(" ");
        }

        //Prints the left pyramid
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        //Prints the space in between the pyramids
        printf("  ");

        //Prints the right pyramid
        for (int z = 0; z < i; z++)
        {
            printf("#");
        }
        printf("\n");
        i++;
    }
}
