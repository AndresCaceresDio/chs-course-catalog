# Program that extracts data from a QuizBowl dataset and creates a frequency csv
# The csv contains information on every question category
# It displays the category name, the year of its first and last appearance
# Also displays its frequency and pattern over time

import json
import numpy as np
import pandas as pd
from scipy.stats import linregress
from collections import defaultdict, Counter
import csv

# Load data from JSON file, you can find similar datasets here: https://sites.google.com/view/qanta/resources
with open('my_data.json', 'r') as file:
    data = json.load(file)

# Extract categories and years
categories = [(q['subcategory'].strip(), q['year']) for q in data['questions']]

category_counts = Counter(categories)
relative_frequencies = {}

for (category, year), count in category_counts.items():
    total = Counter(year for _, year in categories)[year]
    relative_frequency = (count / total) * 100
    relative_frequencies[(category, year)] = relative_frequency

# Initialize default dictionary to track category statistics
category_stats = defaultdict(lambda: {'frequencies': Counter(), 'first': float('inf'), 'last': -1, 'category': ''})

# Populate stats with frequency data
for category, year in categories:
    stats = category_stats[category]
    stats['frequencies'][year] = relative_frequencies[(category, year)]
    stats['first'] = min(stats['first'], year)
    stats['last'] = max(stats['last'], year)

# Create result dictionary
result_dict = {idx: (category,
                     stats['first'],
                     stats['last'],
                     stats['frequencies'],
                     stats['category'])
               for idx, (category, stats) in enumerate(category_stats.items())}

# Output result
csv_filename = 'categories.csv'

# Open the file in write mode
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    # Create a csv writer object
    csvwriter = csv.writer(csvfile)

    # Write the header
    csvwriter.writerow(['Index', 'Category', 'First Appearance', 'Last Appearance', 'Frequency', 'Group'])

    # Write the dictionary to CSV
    i = 0
    list = ["Periodic", "Decreasing", "Periodic", "Constant", "Decreasing", "Sudden onset", "Periodic", "Constant with fluctuating frequency", "Decreasing", "Increasing", "Constant with fluctuating frequency", "Periodic", "Constant with fluctuating frequency", "Constant", "Sudden onset", "Sudden offset", "Increasing", "Decreasing", "Sudden offset", "Increasing", "Increasing", "Periodic", "Sudden onset", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant", "Constant"]
    for key, (answer, first, last, frequency, group) in result_dict.items():
        csvwriter.writerow([key, answer, first, last, frequency, list[i]])
        i += 1
