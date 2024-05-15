#!/usr/bin/env python3
""" Regex-ing"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ function that returns the log messag obfuscated"""
    for field in fields:
        pattern = re.sub(rf"{field}=(.*?)\{separator}",
                         f'{field}={redaction}{separator}', message)
    return pattern
