#!/usr/bin/python

import os
import sys
import optparse
import re
from shutil import copyfile


def main():
    parser = optparse.OptionParser('usage: %prog [options]')
    parser.add_option(
        '-f',
        '--filename',
        dest='filename',
        default='',
        type='string',
        help='Filename of input Bib file.')

    (options, args) = parser.parse_args(sys.argv[1:])

    file_read = open(options.filename)

    entries = []
    entries.append([])
    counter = 0

    for line in file_read:
        line = re.sub(',\n', '', line)
        line = re.sub('\n', '', line)
        if line != '}':  # not end of entry, continue
            entries[counter].append(line)
        else:  # end of entry reached, parse
            entries[counter].pop(0)
            title, author, year, pdf_file = parse_entry(entries[counter])
            write_output
            entries.append([])
            counter += 1

    # print(counter)
    # print(entries[1])


def write_output(title, year, authorlist, abstract, pdf_file):
    filename = ''
    file_write = open(filename, 'w')
    file_write.write('# Summary of ' + title)
    file_write.write('## General Info')
    file_write.write('Title: ' + title)
    file_write.write('Authors: ' + authorlist)
    file_write.write('Year: ' + year)
    file_write.write('\n')
    file_write.write('## Abstract ')
    file_write.write(abstract)


def parse_entry(entry):
    for line in entry:
        substrings = line.split("=")
        print substrings
        if substrings[0] == "title":
            title = substrings[1]
            print title
        elif substrings[0] == "author":
            author = substrings[1]
            print author


if __name__ == '__main__':
    main()
