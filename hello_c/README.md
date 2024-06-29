# Population Growth Calculator

This program calculates the number of years required for a population to grow from a start size to an end size.

## Background

The program simulates the growth of a population. Each year, n / 3 people are born, and n / 4 people pass away. The program takes into account the starting population size and the desired ending population size to determine the number of years required for the population to reach the end size.

## Getting Started

1. Clone this repository to your local machine.
2. Open the terminal and navigate to the directory containing the `population.c` file.
3. Compile the program by running `clang -o population population.c`.
4. Run the program by executing `./population`.

## Usage

When you run the program, it will prompt you for the starting population size. Enter a number greater than or equal to 9. If you enter a number less than 9, the program will re-prompt you until you enter a valid number.

Next, the program will prompt you for the ending population size. Enter a number greater than or equal to the starting population size. If you enter a number less than the starting population size, the program will re-prompt you until you enter a valid number.

The program will then calculate the number of years required for the population to reach the end size and print the result to the terminal.

## Examples

Here are some examples of how the program behaves:

```
$ ./population
Start size: 1200
End size: 1300
Years: 1
```

```
$ ./population
Start size: -5
Start size: 3
Start size: 9
End size: 5
End size: 18
Years: 8
```

```
$ ./population
Start size: 20
End size: 1
End size: 10
End size: 100
Years: 20
```

```
$ ./population
Start size: 100
End size: 1000000
Years: 115
```
