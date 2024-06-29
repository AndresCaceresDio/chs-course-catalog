import json
import ast

# rlhf = []
# with open('gemini.jsonl', 'r', encoding='utf-8') as f:
#     lines = f.readlines()

# newlines= []
# for i in range(len(lines)):
#     if ast.literal_eval(lines[i])['messages'][1]['content'] == "Write an official-style Multistate Bar Examination practice question that tests the subject of Torts":
#         newlines.append(json.dumps(ast.literal_eval(lines[i])['messages'][2]['content']))

# with open('torts.txt', 'r', encoding='utf-8') as file:
#     bad = file.readlines()

# for j in range(281):
#     rlhf.append('{"input_text": "Generate a high quality MBE Torts practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer.", "candidate_0": "' + newlines[j] + '", "candidate_1": "' + json.dumps(bad[j]) + '", "choice": 0}')

# for j in range(281, 562):
#     rlhf.append('{"input_text": "Generate a high quality MBE Torts practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer.", "candidate_0": "' + json.dumps(bad[j]) + '", "candidate_1": "' + newlines[j] + '", "choice": 1}')


# with open('progress.jsonl', 'w') as f:
#     for i in rlhf:
#         f.write(i + "\n")


# with open('prompts.jsonl', 'w') as f:
#     for i in range(504):
#         f.write('{"input_text": "Generate a high quality MBE Civil Procedure practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer."}\n')
#     for i in range(504):
#         f.write('{"input_text": "Generate a high quality MBE Constitutional Law practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer."}\n')
#     for i in range(504):
#         f.write('{"input_text": "Generate a high quality MBE Contracts practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer."}\n')
#     for i in range(504):
#         f.write('{"input_text": "Generate a high quality MBE Criminal Law and Procedure practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer."}\n')
#     for i in range(504):
#         f.write('{"input_text": "Generate a high quality MBE Evidence practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer."}\n')
#     for i in range(504):
#         f.write('{"input_text": "Generate a high quality MBE Real Property practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer."}\n')
#     for i in range(504):
#         f.write('{"input_text": "Generate a high quality MBE Torts practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer."}\n')

# with open('user.jsonl', 'r') as f:
#     l = f.readlines()

# lines = []
# for i in range(len(l)):
#     lines.append(ast.literal_eval(l[i]))

# newlines = []
# for i in range(len(lines)):
#     newlines.append('{"input_text": "' + lines[i]['messages'][1]['content'] + '", "output_text": "' + lines[i]['messages'][2]['content'] + '"}')

# with open('torts.txt', 'w') as f:
#     for i in range(len(newlines)):
#         f.write(str(newlines[i]) + "\n\n")



import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_with_google():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

def get_worksheet(client, spreadsheet_name, sheet_title):
    sheet = client.open(spreadsheet_name).worksheet(sheet_title)
    return sheet

def read_and_split_file(filename, delimiter):
    with open(filename, 'r') as file:
        phrase = """
Please make one more output based on this input:

{"input_text": "Generate a high quality MBE Civil Procedure practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer.", "output_text": }"""
        lines = []
        chunk = ""
        i = 0
        for line in file:
            i += 1
            chunk = chunk + str(line)
            if (i % delimiter) == 0:
                chunk = chunk + phrase
                lines.append(chunk)
                chunk = ""
        if chunk:
            lines.append(chunk)
    return lines

def write_blocks_to_sheet(sheet, blocks):
    batch_size = 3313
    for i in range(0, len(blocks), batch_size):
        end_index = i + batch_size
        values = [[block] for block in blocks[i:end_index]]
        cell_range = 'A{}:A{}'.format(i+1, i + len(values))
        sheet.update(values, cell_range)

def main():
    client = authenticate_with_google()
    sheet = get_worksheet(client, 'GPT-4o', 'Sheet2')
    blocks = read_and_split_file('torts.txt', 230)
    write_blocks_to_sheet(sheet, blocks)

if __name__ == '__main__':
    main()

