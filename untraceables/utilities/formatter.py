# -*- coding: utf-8 -*-

"""
Formatter utility functions.
"""

from __future__ import absolute_import
import os
import re


def show_tables(table_columns):
    """
    Formats the results of SHOW TABLES.

     In the format `table.column`.

    :type tuple
    :param table_columns: Unformatted table columns
    :rtype generator
    :return Formatted table columns
    """

    for table_column in table_columns:
        yield '{0:s}.{1:s}'.format(table_column['TABLE_NAME'], table_column['COLUMN_NAME'])


def table_columns_tsv(database, table_columns):
    """
    Formats the results of SHOW COLUMNS.

     In the format `database<TAB>table<TAB>column`.

    :type str
    :param database: A database name
    :type list
    :param table_columns: Unformatted table columns
    :rtype generator
    :return Formatted table columns
    """

    for table_column in table_columns:
        table, column = table_column.split('.')
        yield '\t'.join((database, table, column))


def randomize_queries(queries):
    """
    Formats the results `query.get_randomize`.

    :type list
    :param queries: Unformatted queries
    :rtype str
    :return Formatted queries
    """

    if len(queries) > 0:
        separator = ';' + os.linesep

        return separator.join(queries) + separator

    return ''


def table_names_from_mydumper_backup(files, suffixed_database):
    """
    Formats the results `filter.table_names_from_mydumper_backup`.

    :type files: generator
    :param files: Filtered file names
    :type suffixed_database: string
    :param suffixed_database: A database name suffixes with a `.` (e.g. `example_com_www.`)
    :rtype generator
    :return Table names
    """

    for file_name in files:
        yield re.sub(r'\.\d+$', '', os.path.splitext(file_name)[0].replace(suffixed_database, ''))


def inclusive_regex_in(inclusive_regex, database_table_delimiter):
    r"""
    Formats an inclusive regex (for input).

    :type inclusive_regex: str
    :param inclusive_regex: An inclusive regex (e.g. `^users\.id$`)
    :type database_table_delimiter: str
    :param database_table_delimiter: A database table delimiter for use in regex (e.g. `\.`)
    :rtype tuple
    :return Splitted table and field regex
    """

    splitted_regex = inclusive_regex.split(database_table_delimiter)
    table_regex = splitted_regex[0]
    field_regex = database_table_delimiter.join(splitted_regex[1:])

    return table_regex, field_regex


def inclusive_regex_out(file_basename, field_regex, database_table_delimiter):
    r"""
    Formats an inclusive regex (for output).

    :type file_basename: str
    :param file_basename: A file (base)name (e.g. `users`)
    :type field_regex: str
    :param field_regex: A field regex (e.g. `id$`)
    :type database_table_delimiter: str
    :param database_table_delimiter: A database table delimiter for use in regex (e.g. `\.`)
    :rtype str
    :return An inclusive regex (e.g. `^users\.id$`)
    """

    return database_table_delimiter.join(['^' + file_basename, field_regex])
