# Program that checks a txt file with a regex pattern
# Any lines that don't follow the pattern are printed to the output file

import re

pattern = r'your_regex_pattern'

with open("your_input.txt", "r", errors="ignore") as file:
    content = file.read()

content = content.replace('\r\n', '\n')

questions = re.split(r', ', content)

list = []
for i in range(len(questions)):
    match_result = re.match(pattern, questions[i], re.MULTILINE  | re.DOTALL)

    if not match_result:
        list.append(i)

with open("your_output.txt", "w") as file:
    for i in list:
        file.write(questions[i])
