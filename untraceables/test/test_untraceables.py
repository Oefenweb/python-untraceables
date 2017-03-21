# -*- coding: utf-8 -*-

import unittest
from glibc_locale_tools.glibc_locale_tools import *
import re


class TestHelperFunctions(unittest.TestCase):

  def test_unicode_decode(self):
    """
    Tests `unicode_decode`.
    """

    # Ascii char
    unicode_char = '002D'
    actual = unicode_decode(unicode_char)
    expected = u'-'
    self.assertEqual(actual, expected)

    # Non-ascii char
    unicode_char = '20AC'
    actual = unicode_decode(unicode_char)
    expected = u'€'
    self.assertEqual(actual, expected)

    # Empty char
    unicode_char = ''
    self.assertRaises(ValueError, unicode_decode, unicode_char)

  def test_unicode_encode(self):
    """
    Tests `unicode_encode`.
    """

    # Ascii char
    char = u'-'
    actual = unicode_encode(char)
    expected = '<U002D>'
    self.assertEqual(actual, expected)

    # Non-ascii char
    char = u'€'
    actual = unicode_encode(char)
    expected = '<U20AC>'
    self.assertEqual(actual, expected)

    # Empty char
    char = u''
    self.assertRaises(TypeError, unicode_encode, char)

  def test_replace_positional(self):
    """
    Tests `replace_positional`.
    """

    original = 'quisquam'
    start = 3
    replacement = 'ct'
    end = 5
    actual = replace_positional(original, start, replacement, end)
    expected = 'quictuam'
    self.assertEqual(actual, expected)

  def test_reverse_iter(self):
    """
    Tests `reverse_iter`.
    """

    actual = reverse_iter(iter([1, 2, 3]))
    expected = iter([3, 2, 1])

    self.assertSequenceEqual(list(actual), list(expected))

  def test_between_quotes_multi_line_multi_value(self):
    """
    Tests BETWEEN_QUOTES_PATTERN.

    Multi line, multi value.
    """

    str = '''
abday   "zo";"ma";"di";/
\t"wo";"do";"vr";/
\t"za"
'''

    actual = re.findall(BETWEEN_QUOTES_PATTERN, str, re.MULTILINE)
    expected = ['zo', 'ma', 'di', 'wo', 'do', 'vr', 'za']
    self.assertSequenceEqual(actual, expected)

  def test_between_quotes_multiline_multiple_single_values(self):
    """
    Tests BETWEEN_QUOTES_PATTERN.

    Multi line, multiple single values.
    """

    str = '''
day     "zondag";/
\t"maandag";/
\t"dinsdag";/
\t"woensdag";/
\t"donderdag";/
\t"vrijdag";/
\t"zaterdag"
'''

    actual = re.findall(BETWEEN_QUOTES_PATTERN, str, re.MULTILINE)
    expected = ['zondag', 'maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag']
    self.assertSequenceEqual(actual, expected)

  def test_between_quotes_single_line_single_value(self):
    """
    Tests BETWEEN_QUOTES_PATTERN.

    Single line, single value
    """

    str = '''
d_t_fmt "%a %d %b %Y %T %Z"
'''

    actual = re.findall(BETWEEN_QUOTES_PATTERN, str, re.MULTILINE)
    expected = ['%a %d %b %Y %T %Z']
    self.assertSequenceEqual(actual, expected)

  def test_between_quotes_single_line_multi_empty_value(self):
    """
    Tests BETWEEN_QUOTES_PATTERN.

    Single line, multi (empty) value.
    """

    str = '''
am_pm   "";""
'''

    actual = re.findall(BETWEEN_QUOTES_PATTERN, str, re.MULTILINE)
    expected = ['', '']
    self.assertSequenceEqual(actual, expected)

  def test_between_quotes_single_line_single_empty_value(self):
    """
    Tests BETWEEN_QUOTES_PATTERN.

    Single line, single (empty) value.
    """

    str = '''
t_fmt_ampm ""
'''

    actual = re.findall(BETWEEN_QUOTES_PATTERN, str, re.MULTILINE)
    expected = ['']
    self.assertSequenceEqual(actual, expected)

  def test_between_quotes_multi_line_single_value(self):
    """
    Tests BETWEEN_QUOTES_PATTERN.

    Multi line, single value.
    """

    str = '''
date_fmt       "%a %b %e/
 %H:%M:%S /
%Z %Y"
'''

    actual = re.findall(BETWEEN_QUOTES_PATTERN, str, re.MULTILINE)
    expected = ['%a %b %e/\n %H:%M:%S /\n%Z %Y']
    self.assertSequenceEqual(actual, expected)

  @unittest.skip("Not supported")
  def test_between_quotes_multi_line_single_value_with_comments(self):
    """
    Tests BETWEEN_QUOTES_PATTERN.

    Multi line, single value, with comments.
    """

    str = '''
% Appropriate AM/PM time representation (%r)
%\t"%I:%M:%S %p"
t_fmt_ampm "%I:%M:%S /
%p"
    '''

    actual = re.findall(BETWEEN_QUOTES_PATTERN, str, re.MULTILINE)
    expected = ['%I:%M:%S /\n%p']
    self.assertSequenceEqual(actual, expected)

  def test_comment_line_with_quotes(self):
    """
    Tests COMMENT_LINE_WITH_QUOTES_PATTERN.
    """

    str = '''
% Appropriate date and time representation (%c)
'''

    self.assertIsNone(re.search(COMMENT_LINE_WITH_QUOTES_PATTERN, str.lstrip('\n')))

    str = '''
%\t"%a %d %b %Y %r %Z"
'''

    self.assertIsNotNone(re.search(COMMENT_LINE_WITH_QUOTES_PATTERN, str.lstrip('\n')))

    str = '''
d_t_fmt "%a %d %b %Y %r %Z"
'''

    self.assertIsNone(re.search(COMMENT_LINE_WITH_QUOTES_PATTERN, str.lstrip('\n')))

    str = '''
%
'''
    self.assertIsNone(re.search(COMMENT_LINE_WITH_QUOTES_PATTERN, str.lstrip('\n')))

  def test_to_decode_pattern(self):
    """
    Tests TO_DECODE_PATTERN.
    """

    str = '''
%a %d %b %Y %T %Z
'''

    actual = re.findall(TO_DECODE_PATTERN, str)
    expected = list(str.strip('\n'))
    self.assertSequenceEqual(actual, expected)

    str = '''
%a %b %e/
 %H:%M:%S /
%Z %Y
'''

    actual = re.findall(TO_DECODE_PATTERN, str)
    expected = list(str.strip('\n').replace('/\n', ''))
    self.assertSequenceEqual(actual, expected)

    str = '''
%a %b %e/ %H:%M:%S /
%Z %Y
'''

    actual = re.findall(TO_DECODE_PATTERN, str)
    expected = list(str.strip('\n').replace('/\n', ''))
    self.assertSequenceEqual(actual, expected)

    str = '''
%m/%d/%Y
'''

    actual = re.findall(TO_DECODE_PATTERN, str)
    expected = list(str.strip('\n'))
    self.assertSequenceEqual(actual, expected)

  def test_between_range(self):
    """
    Tests `between_range`.
    """

    range1 = {'start': 0, 'end': 100}
    range2 = {'start': 5, 'end': 95}

    actual = between_range(range1, range2)
    self.assertTrue(actual)

    range1 = {'start': 0, 'end': 100}
    range2 = {'start': 0, 'end': 100}

    actual = between_range(range1, range2)
    self.assertTrue(actual)

    range1 = {'start': 0, 'end': 49}
    range2 = {'start': 50, 'end': 99}

    actual = between_range(range1, range2)
    self.assertFalse(actual)

    range1 = {'start': 0, 'end': 50}
    range2 = {'start': 50, 'end': 100}

    actual = between_range(range1, range2)
    self.assertFalse(actual)

    range1 = {'start': 0, 'end': 51}
    range2 = {'start': 49, 'end': 100}

    actual = between_range(range1, range2)
    self.assertFalse(actual)

  def test_in_unsafe_spans(self):
    """
    Tests `in_unsafe_spans`.
    """

    match_start = 421
    match_end = 521
    unsafe_spans = [{'start': 521, 'end': 543}, {'start': 612, 'end': 625}, {'start': 685, 'end': 692},
                    {'start': 752, 'end': 768}, {'start': 837, 'end': 909}]

    actual = in_unsafe_spans(match_start, match_end, unsafe_spans)
    self.assertFalse(actual)

    match_start = 522
    match_end = 524
    unsafe_spans = [{'start': 521, 'end': 543}, {'start': 612, 'end': 625}, {'start': 685, 'end': 692},
                    {'start': 752, 'end': 768}, {'start': 837, 'end': 909}]

    actual = in_unsafe_spans(match_start, match_end, unsafe_spans)
    self.assertTrue(actual)

suite = unittest.TestLoader().loadTestsFromTestCase(TestHelperFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
