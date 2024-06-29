import re

# Define the function to add the suffix to the day
def add_date_suffix(match):
    day = match.group(2) # Extract day
    if day.endswith('1') and not day.endswith('11'):
        suffix = 'st'
    elif day.endswith('2') and not day.endswith('12'):
        suffix = 'nd'
    elif day.endswith('3') and not day.endswith('13'):
        suffix = 'rd'
    else:
        suffix = 'th'
    return match.group(1) + " " + day + suffix # Construct the new date string with suffix.

# Define the regex pattern for "Month Day"
date_pattern = re.compile(r'(?<!\d)(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2})(?!\d)')

# Read the contents of the file
with open('questions.txt', 'r') as file:
    content = file.read()

# Use regex sub function to replace dates with their suffixed counterparts
modified_content = date_pattern.sub(add_date_suffix, content)

# Write the new content to 'output.txt'
with open('questions.txt', 'w') as file:
    file.write(modified_content)
