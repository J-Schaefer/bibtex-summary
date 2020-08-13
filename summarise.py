#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import optparse
import re
from shutil import copyfile


def main():
    """
    Main function to control the process.
    :return: None
    """
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


def write_output(out_dir, title='', year='', authorlist='', abstract='', pdf_file=''):
    """
    Writes all the given parameters in an output Markdown file. The
    format is chosen according the standards of Markdown. All options
    except for the out_dir are optional because their availability
    cannot be ensured.
    :param out_dir: Path of the output directory (where the PDFs and
           Markdown files are put)
    :type out_dir: string
    :param title: Title of the bib entry
    :type title: string
    :param year: year of publishing
    :type year: string
    :param authorlist: List of authors with format:
           [[lastname1, firstname1], [lastname2, firstname2]...]
    :type authorlist: list of strings
    :param abstract: Abstract of the publication
    :type abstract: string
    :param pdf_file: Absolute of the associated PDF.
    :type pdf_file: string
    :return: None
    """
    if len(authorlist) <= 1:
        filename = authorlist[0][0] + ' - ' + year + ' - ' + title
    else:
        filename = authorlist[0][0] + ' et al ' + ' - ' + year + ' - ' + title

    path = out_dir + '/' + clean_string(filename)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    file_write = open(path + '.md', 'w')  # open file
    file_write.write('# Summary of ' + title + '\n')  # print caption
    file_write.write('\n')
    file_write.write('## General Info' + '\n')  # print sub caption
    file_write.write('\n')
    file_write.write('Title: ' + title + '\n')  # print title

    # Concatenate authors in one string with format:
    # firstname1 lastname1, firstname2 lastname2, ...
    authors = ''
    for author in authorlist:
        if len(author) == 2:
            authors += author[1] + ' ' + author[0]
        else:
            authors += author[0]

        if author != authorlist[-1]:
            authors += ', '

    file_write.write('Authors: ' + authors + '\n')
    file_write.write('Year: ' + year + '\n')
    file_write.write('\n')
    file_write.write('## Abstract' + '\n')  # Print sub caption
    file_write.write('\n')
    file_write.write(abstract + '\n')

    if os.path.exists(pdf_file):
        copyfile(pdf_file, path + '.pdf')
    file_write.close()


def clean_string(string):
    """
    Clean a given string from Umlauts and unwanted characters to ensure
    compatibility with the file system.
    :param string: String that needs cleaning
    :type string: string
    :return: Cleaned string
    """
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
    """
    Get a list of strings and extract different fields from it.
    :param entry: String including one single entry.
    :type entry: list of strings
    :return: title, authorlist, year, abstract, pdf_file: Field values
             of the bib entries.
    """
    title = ''
    authorlist = ''
    year = ''
    pdf_file = ''
    abstract = ''

    for line in entry:
        substrings = re.split('=', line)
        bib_id = re.sub('\s', '', substrings[0])

        if len(substrings) > 1:
            value = substrings[1]  # get value of the bib field
            value = re.sub('{', '', value)  # remove '{'
            value = re.sub('}', '', value)  # remove '}'

            if bib_id == 'title':
                title = value  # set title

            elif bib_id == 'author':
                # Get list of authors separated by 'and'
                authorlist = value
                # Split at the 'and', authors is then:
                # [lastname, firstname]
                authors = re.split('and', authorlist)
                authorlist = []  # rewrite authorlist as empty list
                for author in authors:
                    # Split author at first and last name and remove
                    # leading and trailing whitespaces
                    author = re.split(',', author)
                    if len(author) > 1:
                        author[0] = author[0].strip()  # remove spaces
                        author[1] = author[1].strip()  # remove spaces
                    print author
                    # Append the author to the authorlist
                    authorlist.append(author)

            elif bib_id == 'date' or bib_id == 'year':
                # Get year from the date/year field
                year = value.split('-')[0]

            elif bib_id == 'abstract':
                abstract = value  # get abstract

            elif bib_id == 'file':
                # Remove first character (space) from the path
                if value[0] == ' ':
                    files = value[1:]
                # Split multiple filenames
                filelist = re.split(';', files)
                for filesingle in filelist:
                    # Get the path of the pdf
                    if '.pdf' in filesingle:
                        pdf_file = filesingle

    return title, authorlist, year, abstract, pdf_file


if __name__ == '__main__':
    main()
