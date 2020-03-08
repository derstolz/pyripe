#!/usr/bin/env python3
import json
import pprint
from os import linesep


# https://ftp.ripe.net/ripe/dbase/

def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--ripe-database',
                        dest='ripe_database',
                        required=True,
                        help='Specify an input path to the RIPE database.')
    parser.add_argument('--search',
                        dest='search',
                        required=True,
                        help='Specify a keyword to search within the given RIPE database.')
    options = parser.parse_args()

    return options


class Section:
    def __init__(self, raw_section):
        self.data = {}

        for section in raw_section.split(linesep):
            chunks = section.split(':', maxsplit=1)
            if len(chunks) == 2:
                key = chunks[0]
                value = chunks[1].strip()
                if key in self.data:
                    self.data[key].append(value)
                else:
                    self.data[key] = [value]

    def __repr__(self):
        return json.dumps(self.data, sort_keys=True, indent=3)


options = get_arguments()

database_file = options.ripe_database
search_keyword = options.search

print(f'Loading the RIPE database: {database_file}')
with open(database_file, 'r', encoding='utf-8', errors='ignore') as ripe_database:
    sections = [Section(section) for section in ripe_database.read().split(linesep * 2)]

for section in sections:
    for key, values in section.data.items():
        for value in values:
            if search_keyword.lower() in value:
                print(section)
