import telebot
import config

from analyse_data import make_data_array_from_parse_data
from draw_graphics import *
from stat_with_frequency import get_stat_with_frequency, get_top_using_words, get_next_prev_words

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    arr_message = message.text.split(' ')[2:]
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                     "бот созданный чтобы быть подопытным кроликом для твоего парсинга википедии. "
                     "Начинаем парсинг!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    link = arr_message[0]
    depth = int(arr_message[1])
    make_data_array_from_parse_data(link, depth)

    bot.send_message(message.chat.id, 'Процесс парсинга успешно завершен, теперь можем посмотреть статистику.')


@bot.message_handler(commands=['describe'])
def describe(message):
    arr_message = message.text.split(' ')[1:]
    if not arr_message:
        draw_stat_length()
        bot.send_message(message.chat.id, 'Предоставляю информацию о количестве слов заданной длины')
        length_stat1 = open('saved_length_statistic1.png', 'rb')
        length_stat2 = open('saved_length_statistic2.png', 'rb')
        length_stat3 = open('saved_length_statistic3.png', 'rb')

        bot.send_photo(message.chat.id, length_stat1)
        bot.send_photo(message.chat.id, length_stat2)
        bot.send_photo(message.chat.id, length_stat3)
    else:
        word = arr_message[0]
        answer = get_top_using_words()
        word_is_in_bad = 0
        word_is_in_not_bad = 0
        without_bad = answer[0]
        with_bad = answer[1]
        kol_in_with_bad = 1
        kol_in_without_bad = 1
        kol_using_times = -1
        for key, value in with_bad.items():
            if key == word:
                word_is_in_bad = 1
                kol_using_times = value
                break
            kol_in_with_bad += 1
        for key, value in without_bad.items():
            if key == word:
                word_is_in_not_bad = 1
                kol_using_times = value
                break
            kol_in_without_bad += 1
        if not (word_is_in_not_bad or word_is_in_bad):
            bot.send_message(message.chat.id, 'Такого слова в статье не существует')
        else:
            answer_string_with = ''
            print(word_is_in_bad, word_is_in_not_bad)
            if word_is_in_bad:
                answer_string_with = 'Слово ' + word + ' занимает ' + str(kol_in_with_bad) + 'место в топе по числу ' \
                                                                                              'использований среди ' \
                                                                                              'выбросов\n '
            answer_string_without = ''
            if word_is_in_not_bad:
                answer_string_without = 'Слово ' + word + ' занимает ' + str(
                    kol_in_without_bad) + 'место в топе по числу ' \
                                          'использований без ' \
                                          'учета ' \
                                          'выбросов\n '
            correct_last_str = 'раз'
            if 2 <= int(kol_using_times) % 10 <= 4 and int(kol_using_times) < 10 or int(kol_using_times) > 20:
                correct_last_str += 'а'
            bot.send_message(message.chat.id, 'Слово <b>' + word + '</b>' +
                             ' встречается ' + str(kol_using_times) + ' ' + correct_last_str, parse_mode='html')
            if answer_string_with != '':
                bot.send_message(message.chat.id, answer_string_with)
            if answer_string_without != '':
                bot.send_message(message.chat.id, answer_string_without)


@bot.message_handler(commands=['word_cloud'])
def word_cloud(message):
    arr_message = message.text.split(' ')
    get_stat_with_frequency()
    try:
        color = arr_message[1]
        make_word_cloud(color)
    except Exception:
        bot.send_message(message.chat.id, 'Некорректный цвет, выберите другой')
    else:
        worldcloud = open('words_cloud.png', 'rb')
        bot.send_message(message.chat.id, 'Облако слов')
        bot.send_photo(message.chat.id, worldcloud)


@bot.message_handler(commands=['freq_bar'])
def freq_bar(message):
    get_stat_with_frequency()
    world_bar = open('words_freq_bar.png', 'rb')
    bot.send_message(message.chat.id, 'Частоты слов')
    bot.send_document(message.chat.id, world_bar)


@bot.message_handler(commands=['top'])
def top(message):
    arr_message = message.text.split(' ')[1:]
    string_ans = ''
    answer = get_top_using_words()
    if arr_message[1] == 'asc':
        string_ans += 'Топ самых частых слов без учета выбросов: ' + '\n'
        kol = 0
        for key, value in answer[0].items():
            correct_last_str = 'раз'
            if 2 <= int(value) % 10 <= 4 and int(value) < 10 or int(value) > 20:
                correct_last_str += 'а'
            string_ans += str(kol + 1) + ') ' + key + ' ' + str(value) + ' ' + correct_last_str + '\n'
            kol += 1
            if kol >= int(arr_message[0]):
                break
    if arr_message[1] == 'desc':
        string_ans += 'Топ самых редких слов без учета выбросов: ' + '\n'
        kol = 0
        for key, value in reversed(answer[0].items()):
            correct_last_str = 'раз'
            if 2 <= int(value) % 10 <= 4 and int(value) < 10 or int(value) > 20:
                correct_last_str += 'а'
            string_ans += str(kol + 1) + ') ' + key + ' ' + str(value) + ' ' + correct_last_str + '\n'
            kol += 1
            if kol >= int(arr_message[0]):
                break
    bot.send_message(message.chat.id, string_ans)


@bot.message_handler(commands=['abc_info'])
def abc_info(message):
    draw_stat_big_small_symb()
    bot.send_message(message.chat.id, 'Информация о использованных буквах')
    small_symb = open('Small_symb_stat.png', 'rb')
    big_symb = open('Big_symb_stat.png', 'rb')
    bot.send_photo(message.chat.id, small_symb)
    bot.send_photo(message.chat.id, big_symb)


@bot.message_handler(commands=['stop_words'])
def stop_words(message):
    stop_words_dict = get_top_using_words()[1]
    bot.send_message(message.chat.id, 'Информация о словах-выбросах')
    string_ans = ''
    for key, value in stop_words_dict.items():
        correct_last_str = 'раз'
        if 2 <= int(value) % 10 <= 4 and int(value) < 10 or int(value) > 20:
            correct_last_str += 'а'
        string_ans += key + ' ' + str(value) + ' ' + correct_last_str + '\n'
    bot.send_message(message.chat.id, string_ans)


@bot.message_handler(commands=['help'])
def help(message):
    file = open('help_info', 'r').readlines()
    str_ans = ''
    for string in file:
        str_ans += string
    bot.send_message(message.chat.id, str_ans)


@bot.message_handler(commands=['next'])
def next_words(message):
    try:
        word = message.text.split(' ')[1]
    except Exception:
        bot.send_message(message.chat.id, 'Введите слово')
        return
    str_ans = ''
    ans = get_next_prev_words(word)[0]
    str_ans += 'Слова, следующие за данным: \n'
    for item in ans:
        if item in str_ans:
            continue
        str_ans += item + '\n'
    bot.send_message(message.chat.id, str_ans)


@bot.message_handler(commands=['prev'])
def prev_words(message):
    try:
        word = message.text.split(' ')[1]
    except Exception:
        bot.send_message(message.chat.id, 'Введите слово')
        return
    str_ans = ''
    ans = get_next_prev_words(word)[1]
    str_ans += 'Слова, перед данным: \n'
    for item in ans:
        if item in str_ans:
            continue
        str_ans += item + '\n'
    bot.send_message(message.chat.id, str_ans)

# RUN
bot.polling(none_stop=True)
