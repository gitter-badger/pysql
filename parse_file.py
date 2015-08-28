#!/usr/bin/env python
"""
    force_cascade.py: Dado un archivo .sql separar las lineas que tengan
    un cierto patron.
"""

import argparse
import os
import mimetypes
from subprocess import call


__author__ = "Flores, Facundo Gabriel"
__version__ = "1.0"
__status__ = "Development"


def process_sql(file_in, pattern):
    if os.path.isfile(file_in):
        if mimetypes.guess_type(file_in)[0] == 'application/x-sql':
            cnt = 0
            file_out = "parsed" + pattern + ".sql"
            with open(file_in, 'r') as inp, open(file_out, 'w') as out:
                array = []
                for line in inp:
                    if line.find(pattern) > 0:
                        out.write(line)
                        #out.write("\n")
                        cnt = cnt + 1
                    else:
                        pass
                print "EXECUTED!"
                inp.close()
                out.close()
                return cnt
        else:
            print file_in + " is not a valid sql file."
            return 0
    else:
        print file_in + " is not an existing regular file."
        return 0


def main():
    app_description = "Write a parsed_PATTERN_.sql file with all patterns found"
    app_description = app_description + " the coincidences"
    parser = argparse.ArgumentParser(description=app_description)
    parser.add_argument('file_in',  help='input file')
    parser.add_argument('pattern', help='Pattern to search')
    args = parser.parse_args()
    cnt_lineas = process_sql(args.file_in, args.pattern)
    print "Number of coincidences: " + str(cnt_lineas) + "."
    call(["atom", "parsed" + args.pattern + ".sql"])

if __name__ == '__main__':
    main()
