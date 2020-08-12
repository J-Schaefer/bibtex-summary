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
            title, authorlist, year, abstract, pdf_file =\
                parse_entry(entries[counter])

            write_output(title=title,
                         year=year,
                         authorlist=authorlist,
                         abstract=abstract,
                         pdf_file=pdf_file)
            entries.append([])
            counter += 1

    # print(counter)
    # print(entries[1])


def write_output(self, title, year, authorlist, abstract, pdf_file):
    directory = 'out/'
    filename = authorlist[0][0] + ' - ' + title

    path = directory + filename

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_write = open(filename + '.md', 'w')
    file_write.write('# Summary of ' + title)
    file_write.write('## General Info')
    file_write.write('Title: ' + title)
    authors = ''
    for author in authorlist:
        if len(author) == 2:
            authors += author[1] + author[0]
        else:
            authors += author[0]

    file_write.write('Authors: ' + authors)
    file_write.write('Year: ' + year)
    file_write.write('\n')
    file_write.write('## Abstract ')
    file_write.write(abstract)
    copyfile(pdf_file, filename + '.pdf')


def parse_entry(entry):
    title = ''
    year = ''
    pdf_file = ''
    abstract = ''

    for line in entry:
        substrings = re.split('=', line)
        bib_id = re.sub(' ', '', substrings[0])

        if len(substrings) > 1:
            value = substrings[1]
            value = re.sub('{', '', value)
            value = re.sub('}', '', value)
            # print id
            if bib_id == 'title':
                title = value
                # print title
            elif bib_id == 'author':
                authorlist = value  # list of authors separated by 'and'
                # Split at the 'and', authors is then: lastname, firstname
                authors = re.split('and', authorlist)
                authorlist = []  # rewrite authorlist as empty list
                for author in authors:
                    author = re.sub(' ', '', author)
                    author = re.split(',', author)
                    authorlist.append(author)
                # print authorlist
            elif bib_id == 'date':
                year = value.split('-')[0]
                # print year
            elif bib_id == 'abstract':
                abstract = value
            elif bib_id == 'file':
                files = value[1:]
                filelist = re.split(';', files)
                for filesingle in filelist:
                    if '.pdf' in filesingle:
                        pdf_file = filesingle
                print pdf_file

    return title, authorlist, year, abstract, pdf_file

if __name__ == '__main__':
    main()
