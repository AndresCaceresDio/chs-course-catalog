// Project description can be found at: https://cs50.harvard.edu/x/2023/psets/1/cash/

#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);
int a = 0;
int b = -1;
int c = -1;
int d = -1;
int e = -1;

int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}

//Prompts the user to input the amount of change that is owed
int get_cents(void)
{
    do
    {
        a = get_int("Change Owed: ");
    }
    while (a < 0);
    return a;
}

//Calculates the amount of quarters needed
int calculate_quarters(int cents)
{
    for (int i = 0; i <= cents; i = i + 25)
    {
        b = b + 1;
    }
    return b;
}

//Calculates the amount of dimes needed
int calculate_dimes(int cents)
{
    for (int i = 0; i <= cents; i = i + 10)
    {
        c = c + 1;
    }
    return c;
}

//Calculates the amount of nickels needed
int calculate_nickels(int cents)
{
    for (int i = 0; i <= cents; i = i + 5)
    {
        d = d + 1;
    }
    return d;
}

//Calculates the amount of pennies needed
int calculate_pennies(int cents)
{
    for (int i = 0; i <= cents; i++)
    {
        e = e + 1;
    }
    return e;
}
