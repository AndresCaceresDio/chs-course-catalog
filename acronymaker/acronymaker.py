from itertools import product, permutations, islice

def is_word(word, spell):
    word_lower = word.lower()
    is_valid = word_lower in spell
    return is_valid

def generate_acronym(acronym_tuple, revised_synonyms, spell):
    acronym = ''.join(word[0].upper() for word in acronym_tuple)
    if is_word(acronym, spell):
        context = ['{} (synonym for {})'.format(word, syn_list[-1]) if word in syn_list and word != syn_list[-1] else word
                     for word in acronym_tuple for syn_list in revised_synonyms if word in syn_list]
        return f"{acronym} [{', '.join(context)}]"
    return None

def generate_acronyms(revised_synonyms, ordered='no', offset=0, limit=30, spell=None):
    acronym_generator = islice(product(*revised_synonyms), offset, None) if ordered == "yes" else islice((
                        prod for perm in permutations(revised_synonyms) for prod in product(*perm)), offset, None)
    valid_acronyms = []
    next_offset=offset
    for acronym_tuple in acronym_generator:
        next_offset+=1
        acronym_result = generate_acronym(acronym_tuple, revised_synonyms, spell)
        if acronym_result:
            valid_acronyms.append(acronym_result)
            if len(valid_acronyms) >= limit:
                break

    return valid_acronyms, next_offset

def generate_acronyms_heavy(revised_synonyms, ordered='no', offset=0, limit=30, spell=None):
    acronym_generator = islice(product(*revised_synonyms), offset, None) if ordered == "yes" else islice((
                        prod for perm in permutations(revised_synonyms) for prod in product(*perm)), offset, offset+1000000)
    valid_acronyms = []
    next_offset=offset
    for acronym_tuple in acronym_generator:
        next_offset+=1
        acronym_result = generate_acronym(acronym_tuple, revised_synonyms, spell)
        if acronym_result:
            valid_acronyms.append(acronym_result)
            if len(valid_acronyms) >= limit:
                break

    return valid_acronyms, next_offset
