#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long a;
    do
    {
        a = get_long("Start size: ");
    }
    while (a < 9);

    long b;
    do
    {
        b = get_long("End size: ");
    }
    while (b < a);

    float x = 0;
    long n = 0;

    do
    {
        x = a + ((a / 3) - (a / 4) );
        a = x;
        n++;
    }
    while (x < b);

    printf("Years: %li\n", n);
}
