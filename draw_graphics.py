import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from analyse_data import get_data_arr


def find_abc_in_df():
    data_arr = get_data_arr()
    df = pd.DataFrame(data_arr, columns=['id', 'word', 'length'])
    lang = 'abcdefghijklmnopqrstuvwxyz'
    LANG = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    LANG = LANG[::-1]
    kol_up = {}
    kol_down = {}
    for symb in lang:
        kol_down[symb] = 0
    for symb in LANG:
        kol_up[symb] = 0
    for expr in df['word']:
        for symb in expr:
            if symb in lang or symb in LANG:
                if symb.isupper():
                    kol_up[symb] += 1
                else:
                    kol_down[symb] += 1
    return kol_up, kol_down


def draw_stat_big_small_symb():
    fig = plt.figure(figsize=(20, 20))
    answer = find_abc_in_df()
    plt.bar(range(len(answer[0])), list(answer[0].values()), align='center')
    plt.xticks(range(len(answer[0])), list(answer[0].keys()))
    plt.savefig('Big_symb_stat.png')
    plt.bar(range(len(answer[1])), list(answer[1].values()), align='center')
    plt.xticks(range(len(answer[1])), list(answer[1].keys()))
    plt.savefig('Small_symb_stat.png')


def make_word_cloud(color):
    data_arr = get_data_arr()
    df = pd.DataFrame(data_arr, columns=['id', 'word', 'length'])
    text_raw = " ".join(df['word'].drop_duplicates())
    wordcloud = WordCloud(background_color=color, stopwords=STOPWORDS).generate(text_raw)
    wordcloud.to_file('words_cloud.png')


def draw_stat_length():
    data_arr = get_data_arr()
    figure, axes = plt.subplots(3, figsize=(50, 50))
    ax1 = axes[0]
    ax2 = axes[1]
    ax3 = axes[2]

    ax1.set_xlabel('Length', fontsize=20)
    ax1.set_ylabel('Number words', fontsize=20)

    # ax1.xaxis.set_major_locator(ticker.MultipleLocator(1))
    # ax1.yaxis.set_major_locator(ticker.MultipleLocator(10))

    ax2.set_xlabel('Number words', fontsize=20)
    ax2.set_ylabel('Length', fontsize=20)
    # ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))

    df = pd.DataFrame(data_arr, columns=['id', 'word', 'length'])

    df.length.value_counts().sort_index(ascending=False).plot(ax=ax1, grid=True, fontsize=20)

    extent = ax1.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    ax1.figure.savefig('saved_length_statistic1.png', bbox_inches=extent.expanded(1.1, 1.2))

    df.length.value_counts().sort_index(ascending=False).plot(ax=ax2, kind='barh', grid=True, fontsize=20)
    extent = ax2.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    ax2.figure.savefig('saved_length_statistic2.png', bbox_inches=extent.expanded(1.1, 1.2))

    df.length.value_counts().sort_index(ascending=False).plot(ax=ax3, kind='pie',
                                                              autopct='%1.1f%%',
                                                              shadow=True,
                                                              ylabel='Length',
                                                              grid=True,
                                                              fontsize=20)
    extent = ax3.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    ax3.figure.savefig('saved_length_statistic3.png', bbox_inches=extent.expanded(1.1, 1.2))
    plt.close()
