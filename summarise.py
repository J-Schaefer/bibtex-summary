#!/usr/bin/python

import os
import sys
import optparse
import re


def main():
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option(
        "-f",
        "--filename",
        dest="filename",
        default="",
        type="string",
        help="Filename of input Bib file.")

    (options, args) = parser.parse_args(sys.argv[1:])

    file_read = open(options.filename)

    entries = []
    entries.append([])
    counter = 0

    for line in file_read:
        line = re.sub(',\n', '', line)
        line = re.sub('\n', '', line)
        if line <> "}":
            entries[counter].append(line)
        else:
            entries[counter].pop(0)
            parse_entry(entries[counter])
            entries.append([])
            counter += 1

    # print(counter)
    # print(entries[1])


def write(filename, title, year, authorlist, abstract):
    file_write = open(filename, "a")
    file_write.write("# Summary of " + title)
    file_write.write("## General Info")
    file_write.write("Title: " + title)
    file_write.write("Authors: " + authorlist)
    file_write.write("Year: " + year)
    file_write.write()
    file_write.write("## Abstract ")
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
