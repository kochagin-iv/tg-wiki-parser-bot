import pandas as pd
import matplotlib.pyplot as plt
from analyse_data import get_data_arr
import matplotlib.ticker as ticker


def get_next_prev_words(word):
    data_arr = get_data_arr()
    df = pd.DataFrame(data_arr, columns=['id', 'word', 'length'])
    list_words = df['word'].to_list()
    next_words = []
    prev_words = []
    if len(list_words) > 1 and list_words[0] == word:
        next_words.append(list_words[1])
    if len(list_words) > 1 and list_words[len(list_words) - 1] == word:
        prev_words.append(list_words[len(list_words) - 2])

    for i in range(1, len(list_words) - 1):
        if list_words[i] == word:
            next_words.append(list_words[i + 1])
            prev_words.append(list_words[i - 1])
    return prev_words, next_words


def get_top_using_words():
    data_arr = get_data_arr()
    df = pd.DataFrame(data_arr, columns=['id', 'word', 'length'])
    # print(len(df))
    frequency_df = df.word.value_counts().to_frame()
    frequency_df_without_bad_words = frequency_df[frequency_df['word'].apply(
        lambda x: df.word.value_counts().mean() - 3 < x < df.word.value_counts().mean() + 3)]
    frequency_df_with_bad_words = frequency_df[frequency_df['word'].apply(
        lambda x: df.word.value_counts().mean() - 3 >= x or x >= df.word.value_counts().mean() + 3)]
    return frequency_df_without_bad_words['word'].to_dict(), frequency_df_with_bad_words['word'].to_dict()


def get_stat_with_frequency():
    data_arr = get_data_arr()
    df = pd.DataFrame(data_arr, columns=['id', 'word', 'length'])
    frequency_df = df.word.value_counts().to_frame()
    a = frequency_df['word'].to_dict()

    xval = []
    yval = []
    for key, value in a.items():
        xval.append(value)
        yval.append(key)

    x = frequency_df['word']
    e = x.mean()
    frequency_df['word'] = round(x - e, 2)
    frequency_df['colors'] = ['red' if x < 0 else 'green' for x in frequency_df['word']]

    plt.figure(figsize=(200, 200), dpi=80)
    plt.hlines(y=frequency_df.index, xmin=0, xmax=frequency_df.word)
    for x, y, tex in zip(frequency_df.word, frequency_df.index, frequency_df.word):
        t = plt.text(x, y, tex, horizontalalignment='right' if x < 0 else 'left',
                     verticalalignment='center', fontdict={'color': 'red' if x < 0 else 'green', 'size': 12})

    plt.yticks(frequency_df.index, frequency_df.index, fontsize=12)
    plt.title('Diverging Text Bars of Car Mileage', fontdict={'size': 20})
    plt.grid(linestyle='--', alpha=0.5)
    # plt.xlim(-2.5, 2.5)
    plt.savefig('words_freq_bar.png')
