import re

pattern = r'^Question \([^)]+\): [A-Z].*[\.\?!"]\n\n[A-Z][^.!]*\n\n\(A\) .+[\.\?!"]\n\(B\) .+[\.\?!"]\n\(C\) .+[\.\?!"]\n\(D\) .+[\.\?!"]\n\n\n$'

with open("clean.txt", "r", errors="ignore") as file:
    content = file.read()

content = content.replace('\r\n', '\n')

questions = re.split(r'(?<=\n\n)Question \(', content)

questions = [questions[0]] + ['Question (' + q for q in questions[1:]]

list = []
for i in range(len(questions)):
    match_result = re.match(pattern, questions[i], re.MULTILINE  | re.DOTALL)

    if not match_result:
        list.append(i)

with open("cleaning.txt", "w") as file:
    for i in list:
        file.write(questions[i])
