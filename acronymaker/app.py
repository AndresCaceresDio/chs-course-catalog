from flask import Flask, render_template, request, jsonify
from acronymaker import generate_acronyms, generate_acronyms_heavy
import math
from spellchecker import SpellChecker

app = Flask(__name__)

duplicate_acronyms = set()

def validate_input(ordered, words_list, synonyms_list):
    revised_synonyms = []
    total_length = 0
    for i in range(len(synonyms_list)):
        revised_list = synonyms_list[i]
        revised_list.append(words_list[i])
        revised_synonyms.append(revised_list)
        total_length += len(revised_list)

    if ordered == "no":
        try:
            n = total_length / len(revised_synonyms)
        except ZeroDivisionError:
            return [revised_synonyms]
        possibilities = math.factorial(len(revised_synonyms))*(n**len(revised_synonyms))
        if len(revised_synonyms) < 8:
            return [revised_synonyms]
        else:
            return revised_synonyms, possibilities

    elif ordered == "yes":
        return [revised_synonyms]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_synonyms():
    data = request.get_json()
    words_list = data['words_list']
    synonyms_list = data['synonyms_list']
    ordered = data.get('ordered', 'no')
    offset = data.get('offset', 0)
    language = data['language']
    spell = SpellChecker(language)
    checker_list = validate_input(ordered, words_list, synonyms_list)
    if len(checker_list) == 2:
        checker = checker_list[0]
        possibilities = checker_list[1]
    else:
        checker = checker_list[0]
        possibilities = None
    revised_synonyms = checker
    acronym_results = []
    next_offset = offset
    if len(checker) > 7:
        iter_counter = 0
        while not acronym_results:
            acronym_results, next_offset = generate_acronyms_heavy(revised_synonyms, ordered, next_offset, limit=30, spell=spell)
            iter_counter += 1000000
            if iter_counter == round(possibilities / 1000) * 1000:
                break
            if acronym_results:
                if acronym_results[0][:len(words_list)] in duplicate_acronyms:
                    acronym_results = None
                else:
                    duplicate_acronyms.add((acronym_results[0][:len(words_list)]))
    else:
        acronym_results, next_offset = generate_acronyms(revised_synonyms, ordered, offset, limit=30, spell=spell)
    return jsonify({'status': 'success', 'acronyms': acronym_results, 'next_offset': next_offset})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
