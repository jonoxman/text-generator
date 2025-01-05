from nltk.corpus import wordnet as wn
import re
def nouns_list(input_str):
    """
    Return a list of all the nouns in the input string.
    
    Args:
        input_str (str): the string from which nouns should be extracted.
    """
    # Get a set of all nouns
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    
    # Remove the nonalphabetical words from the input string and add the remaining words to a set
    regex = re.compile('[^a-zA-Z]')
    words = input_str.split(' ')
    result = set()
    for word in words:
        result.add(regex.sub('', word))
    return result.intersection(nouns)