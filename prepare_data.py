import string

from DB.DBfunctions import get_words, get_words_dictionary


def format_dish_names(dishes):
    d = [filter_name(x) for x in dishes]
    d = correct_words(d)
    d = remove_rarely_used_words(d)
    return d


def filter_name(name):
    name = name.lower()
    name = name.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    name = name.translate(str.maketrans('', '', string.digits))
    name = name.translate(str.maketrans('ăâşșîţț', 'aassitt'))
    return ' '.join(name.split())


def correct_words(names_list):
    words_dict = get_words_dictionary()
    misspelled_words = [x[0] for x in words_dict]
    words_dict = {key: value for (key, value) in words_dict}
    # bizz_words = ['alegere', 'chorizo', 'ciabatta', 'condimentat', 'ketchup', 'necondimentati', 'nepicant', 'sandwich']
    bizz_words = ['alegere', 'ciabatta', 'condimentat', 'ketchup', 'necondimentati', 'nepicant']
    words_to_remove = ['al', 'buc', 'con', 'e', 'g', 'kcal', 'new', 'sau'] + bizz_words

    new_list = [
        ' '.join([w if w not in misspelled_words else words_dict[w] for w in name.split() if w not in words_to_remove])
        for name in names_list]
    return new_list


def remove_rarely_used_words(names_list):
    words = get_words()
    # replace unknown words with <UNK>
    new_list = [' '.join([x if x in words else '<UNK>' for x in name.split()]) for name in names_list]
    # remove unknown words
    # new_list = [' '.join([x for x in name.split() if x in words]) for name in names_list]
    return new_list


def pad_names(name):
    limit = 20
    words = name.split()
    if len(words) >= limit:
        name = ' '.join(words[:limit])
    else:
        padding = ['<PAD>'] * (limit - len(words))
        name = ' '.join(words + padding)
    return name
