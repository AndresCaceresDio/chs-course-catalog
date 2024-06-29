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

def unscramble_jsonl(input_file, output_file):
    with open(input_file, 'r') as f:
        line = f.readlines()

    lines = []
    for i in range(len(line)):
        lines.append(ast.literal_eval(line[i]))

    civpro = []
    conlaw = []
    contracts = []
    crimlaw = []
    evidence = []
    realprop = []
    torts = []

    for i in range(len(lines)):
        if lines[i]['messages'][1]['content'] == "Write an official-style Multistate Bar Examination practice question that tests the subject of Civil Procedure":
            civpro.append(lines[i])
        elif lines[i]['messages'][1]['content'] == "Write an official-style Multistate Bar Examination practice question that tests the subject of Constitutional Law":
            conlaw.append(lines[i])
        elif lines[i]['messages'][1]['content'] == "Write an official-style Multistate Bar Examination practice question that tests the subject of Contracts":
            contracts.append(lines[i])
        elif lines[i]['messages'][1]['content'] == "Write an official-style Multistate Bar Examination practice question that tests the subject of Criminal Law and Procedure":
            crimlaw.append(lines[i])
        elif lines[i]['messages'][1]['content'] == "Write an official-style Multistate Bar Examination practice question that tests the subject of Evidence":
            evidence.append(lines[i])
        elif lines[i]['messages'][1]['content'] == "Write an official-style Multistate Bar Examination practice question that tests the subject of Real Property":
            realprop.append(lines[i])
        elif lines[i]['messages'][1]['content'] == "Write an official-style Multistate Bar Examination practice question that tests the subject of Torts":
            torts.append(lines[i])

    questions = []
    for i in range(len(civpro)):
        questions.append(civpro[i])
    for i in range(len(conlaw)):
        questions.append(conlaw[i])
    for i in range(len(contracts)):
        questions.append(contracts[i])
    for i in range(len(crimlaw)):
        questions.append(crimlaw[i])
    for i in range(len(evidence)):
        questions.append(evidence[i])
    for i in range(len(realprop)):
        questions.append(realprop[i])
    for i in range(len(torts)):
        questions.append(torts[i])

    with open(output_file, 'w') as f:
        for i in range(len(questions)):
            f.write(str(json.dumps(questions[i])) + "\n")

# scramble_jsonl('gemini.jsonl', 'gemini.jsonl')
unscramble_jsonl('bison.jsonl', 'bison.jsonl')
