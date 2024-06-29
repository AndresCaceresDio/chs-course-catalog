from cs50 import get_string

text = get_string("Text: ")
letters = 0
sentences = 0
words = 1

for i in range(len(text)):
    if ord(text[i]) >= 65 and ord(text[i]) <= 122:
        letters += 1
    elif text[i] == '.' or text[i] == '?' or text[i] == '!':
        sentences += 1
    elif text[i] == ' ' or text[i] == '"' and ord(text[i + 1]) >= 65 and ord(text[i + 1]) <= 122:
        words += 1
L = (letters / words) * 100
S = (sentences / words) * 100
x = (0.0588 * L)
y = (0.296 * S)

readability = x - y - 15.8

if readability > 16:
    print("Grade 16+")
elif readability < 1:
    print("Before Grade 1")
else:
    print("Grade", round(readability))