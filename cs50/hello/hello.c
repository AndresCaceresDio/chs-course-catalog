#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Asks for name and stores answer in a variable, name
    string name = get_string("What is your name? ");
    //Prints out a greeting specific to the inputted name
    printf("hello, %s\n", name);
}
