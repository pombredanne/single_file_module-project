#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module is to make regular expression easier to use.
With some built-in compiled pattern, we can use human language-like syntax to 
generate re pattern.
"""

from __future__ import print_function, unicode_literals
import re


def extract_by_prefix_surfix(text, prefix, surfix, minlen=None, maxlen=None):
    """Extract the text in between a prefix and surfix. It use non-greedy match.

    :param text: text body
    :type text: str

    :param prefix: the prefix
    :type prefix: str

    :param surfix: the surfix
    :type surfix: str

    :param minlen: the min matched string length
    :type minlen: int

    :param maxlen: the max matched string length
    :type maxlen: int
    """
    if minlen is None:
        minlen = 0
    if maxlen is None:
        maxlen = 2 ** 30
    pattern = r"""(?<=%s)[\s\S]{%s,%s}?(?=%s)""" % (
        prefix, minlen, maxlen, surfix)
    return re.findall(pattern, text)


def extract_number(text):
    result = list()
    chunk = list()
    valid_char = set(".1234567890")
    for char in text:
        if char in valid_char:
            chunk.append(char)
        else:
            result.append("".join(chunk))
            chunk = list()
    result.append("".join(chunk))

    result_new = list()
    for number in result:
        if "." in number:
            try:
                result_new.append(float(number))
            except:
                pass
        else:
            try:
                result_new.append(int(number))
            except:
                pass

    return result_new

#--- Unittest ---


def test_extract_by_prefix_surfix():
    assert extract_by_prefix_surfix(
        text="<div>Hello</div><div>World</div>",
        prefix="<div>", surfix="</div>"
    ) == ["Hello", "World"]


def test_extract_number():
    for i, j in zip(
        extract_number(
            "Price is $25.99, age is 18, quarter is .25, one is 1."),
        [25.99, 18, 0.25, 1.0],
    ):
        assert abs(i - j) <= 0.0001

if __name__ == "__main__":
    test_extract_by_prefix_surfix()
    test_extract_number()
