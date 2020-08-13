#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    parser.add_option(
        '-o',
        '--outdir',
        dest='outdir',
        default='out',
        type='string',
        help='Directory name for output.')

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
                         pdf_file=pdf_file,
                         out_dir=options.outdir)
            entries.append([])
            counter += 1


def write_output(title, year, authorlist, abstract, pdf_file, out_dir):
    if len(authorlist) <= 1:
        filename = authorlist[0][0] + ' - ' + year + ' - ' + title
    else:
        filename = authorlist[0][0] + ' et al ' + ' - ' + year + ' - ' + title

    path = out_dir + '/' + clean_string(filename)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    file_write = open(path + '.md', 'w')
    file_write.write('# Summary of ' + title + '\n')
    file_write.write('\n')
    file_write.write('## General Info' + '\n')
    file_write.write('\n')
    file_write.write('Title: ' + title + '\n')
    authors = ''
    for author in authorlist:
        if len(author) == 2:
            authors += author[1] + author[0]
        else:
            authors += author[0]

    file_write.write('Authors: ' + authors + '\n')
    file_write.write('Year: ' + year + '\n')
    file_write.write('\n')
    file_write.write('## Abstract' + '\n')
    file_write.write('\n')
    file_write.write(abstract + '\n')

    if os.path.exists(pdf_file):
        copyfile(pdf_file, path + '.pdf')
    file_write.close()


def clean_string(string):
    string = re.sub('Ä', 'Ae', string)
    string = re.sub('ä', 'ae', string)
    string = re.sub('Ö', 'Oe', string)
    string = re.sub('ö', 'oe', string)
    string = re.sub('Ü', 'Ue', string)
    string = re.sub('Ü', 'ue', string)
    string = re.sub('ß', 'ss', string)
    # Avoid slashes in names because they represent sub-dirs
    string = re.sub('/', ' ', string)
    return string


def parse_entry(entry):
    title = ''
    authorlist = ''
    year = ''
    pdf_file = ''
    abstract = ''

    for line in entry:
        substrings = re.split('=', line)
        bib_id = re.sub('\s', '', substrings[0])

        if len(substrings) > 1:
            value = substrings[1]
            value = re.sub('{', '', value)
            value = re.sub('}', '', value)

            if bib_id == 'title':
                title = value

            elif bib_id == 'author':
                authorlist = value  # list of authors separated by 'and'
                # Split at the 'and', authors is then: lastname, firstname
                authors = re.split('and', authorlist)
                authorlist = []  # rewrite authorlist as empty list
                for author in authors:
                    author = re.sub(' ', '', author)
                    author = re.split(',', author)
                    authorlist.append(author)

            elif bib_id == 'date' or bib_id == 'year':
                year = value.split('-')[0]

            elif bib_id == 'abstract':
                abstract = value
            elif bib_id == 'file':
                files = value[1:]
                filelist = re.split(';', files)
                for filesingle in filelist:
                    if '.pdf' in filesingle:
                        pdf_file = filesingle

    return title, authorlist, year, abstract, pdf_file


if __name__ == '__main__':
    main()
