#!/usr/bin/env python3
""" Regex-ing"""

from typing import List
import mysql.connector
import logging
import re
import os

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ function that returns the log messag obfuscated"""
    for field in fields:
        pattern = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return pattern


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialization"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records using filter_datum"""
        formatted_record = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            formatted_record, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ function that returns a logger object"""
    user_data = logging.getLogger("user_data")
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data.addHandler(handler)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ function that returns a connector to the database"""
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    if host is None:
        host = "localhost"
    user = os.getenv("PERSONAL_DATA_DB_USERNAME")
    if user is None:
        user = "root"
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    if password is None:
        password = ""
    db = os.getenv("PERSONAL_DATA_DB_NAME")
    dbConnection = mysql.connector.connect(
        host=host, user=user, password=password, database=db
    )
    return dbConnection


def main() -> None:
    """ main function"""
    pass
    """db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        print(row)
    cursor.close()
    db.close()"""


if __name__ == '__main__':
    main()
