# Program that scrambles the lines of a jsonl file to a random order

import json
import ast
import random

def scramble_jsonl(input_file, output_file):
    # Read the lines from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Scramble the lines
        random.shuffle(lines)
        # Write the scrambled lines to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines: f.write(line)

scramble_jsonl('your_file.jsonl', 'your_file.jsonl')
