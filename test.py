import unittest
from unittest import mock
from unittest.mock import patch

from draw_graphics import find_abc_in_df
from stat_with_frequency import *
import analyse_data


def arr_for_test_next_words():
    df = [[1, 'word1', 5],
          [2, 'word2', 5],
          [3, 'word3', 5],
          [4, 'aaa', 3],
          [5, 'word4', 5],
          [6, 'word4', 5]]
    return df


def arr_with_many_not_differ_words():
    df = []
    for i in range(10000):
        cur_arr = []
        df.append([i + 1, 'word', 4])
    df.append([10001, 'abacaba', 7])
    return df


def arr_for_testing_abs():
    df = []
    word1 = 'abcdefghijklmnopqrstuvwxyz'
    word2 = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    for i in range(100000):
        df.append([i + 1, word1, len(word1)])
    for i in range(100000, 200000):
        df.append([i + 1, word2, len(word2)])
    return df


class MyTestCase(unittest.TestCase):
    def setUp(self):
        analyse_data.data_arr = arr_for_test_next_words()

    def test_prev_next_words(self):
        self.assertEqual(get_next_prev_words('word1'), ([], ['word2']))
        self.assertEqual(get_next_prev_words('word2'), (['word1'], ['word3']))
        self.assertEqual(get_next_prev_words('word3'), (['word2'], ['aaa']))
        self.assertEqual(get_next_prev_words('aaa'), (['word3'], ['word4']))
        self.assertEqual(get_next_prev_words('bad_word'), ([], []))
        self.assertEqual(get_next_prev_words('word4'), (['word4', 'aaa'], ['word4']))

    def test_get_top_using_words(self):
        ans_for_test = get_top_using_words()
        self.assertEqual(ans_for_test[0], {'aaa': 1,
                                           'word1': 1,
                                           'word2': 1,
                                           'word3': 1,
                                           'word4': 2})
        self.assertEqual(ans_for_test[1], {})
        analyse_data.data_arr = arr_with_many_not_differ_words()
        ans_for_test = get_top_using_words()
        self.assertEqual(ans_for_test[0], {})
        self.assertEqual(ans_for_test[1], {'word': 10000,
                                           'abacaba': 1})

    def test_find_abc_in_df(self):
        analyse_data.data_arr = arr_for_testing_abs()
        ans_for_test = find_abc_in_df()
        correct_ans_big = {}
        correct_ans_small = {}

        for i in 'ZYXWVUTSRQPONMLKJIHGFEDCBA':
            correct_ans_big[i] = 100_000
        for i in 'abcdefghijklmnopqrstuvwxyz':
            correct_ans_small[i] = 100_000

        self.assertEqual(ans_for_test[0], correct_ans_big)
        self.assertEqual(ans_for_test[1], correct_ans_small)


if __name__ == '__main__':
    unittest.main()
