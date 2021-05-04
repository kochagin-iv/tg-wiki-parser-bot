from parse_wiki import parse, get_str_full_text

data_arr = []


def get_data_arr():
    global data_arr
    return data_arr


def make_data_array_from_parse_data(url, depth):
    parse(url, depth)
    global data_arr
    kol_words = 0
    str_full_text = get_str_full_text()
    for word in str_full_text:
        if len(word) > 40:
            continue
        kol_upper_symb = 0
        kol_no_upper_symb = 0

        for symbol in word:
            if symbol.isupper():
                kol_upper_symb += 1
            else:
                kol_no_upper_symb += 1
            if kol_no_upper_symb >= 2 and kol_upper_symb >= 2:
                break
        if kol_no_upper_symb >= 2 and kol_upper_symb >= 2:
            continue

        current_arr = [kol_words]
        kol_words += 1
        current_arr.append(word)
        current_arr.append(len(word))
        data_arr.append(current_arr)
