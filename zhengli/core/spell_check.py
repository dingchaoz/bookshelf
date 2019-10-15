import os

from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

max_edit_distance_dictionary = 2
prefix_length = 7
# create object
sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
# load dictionary
dictionary_path = os.path.join(os.path.dirname(__file__),
                               "../data/frequency_dictionary_en_82_765.txt")


def correct_text(input_term=("whereis th elove hehad dated forImuch of thepast who "
                             "couqdn'tread in sixtgrade and ins pired him")):

    print('correcting text....')
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):

        return

    # lookup suggestions for multi-word input strings (supports compound
    # splitting & merging)
    # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 2
    suggestions = sym_spell.lookup_compound(input_term,
                                            max_edit_distance_lookup)
    # display suggestion term, edit distance, and term frequency
    for suggestion in suggestions:
        print("extracted text: {}".format(suggestion.term))

    return suggestion.term
