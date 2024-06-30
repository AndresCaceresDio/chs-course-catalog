# Project description can be found at: https://cs50.harvard.edu/x/2023/psets/6/dna/

import csv
import sys


def main():

    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    csv_file = sys.argv[1]
    csv_data = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            for i in row:
                csv_data.append(i)

    csv_data.append(" ")
    txt_file = sys.argv[2]
    txt_data = open(txt_file, "r").read()

    match1 = str(longest_match(txt_data, "AGATC"))
    match2 = str(longest_match(txt_data, "TTTTTTCT"))
    match3 = str(longest_match(txt_data, "AATG"))
    match4 = str(longest_match(txt_data, "TCTAG"))
    match5 = str(longest_match(txt_data, "GATA"))
    match6 = str(longest_match(txt_data, "TATC"))
    match7 = str(longest_match(txt_data, "GAAA"))
    match8 = str(longest_match(txt_data, "TCTG"))

    for i in range(len(csv_data)):

        if (csv_data[i] in match1 and csv_data[i + 1] in match2 and csv_data[i + 2] in match3 and csv_data[i + 3]
        in match4 and csv_data[i + 4] in match5 and csv_data[i + 5] in match6 and csv_data[i + 6] in match7 and
        csv_data[i + 7] in match8):
            print(csv_data[i - 1])
            return
        elif int(match2) == 0:
            x = match3
            y = match6
            if csv_data[i] in match1 and csv_data[i + 1] in x and csv_data[i + 2] in y:
                print(csv_data[i - 1])
                return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
