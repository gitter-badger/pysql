#!/usr/bin/env python
"""
    force_cascade.py: Dado un archivo .sql en texto plano anade la sentencia
    ON DELETE CASCADE para todas las referencias existentes (FKs).
"""

import argparse
import os
import mimetypes
from subprocess import call

__author__ = "Flores, Facundo Gabriel"
__version__ = "1.0"
__status__ = "Development"


def add_ondelete(l):
    return l[:len(l) - 2] + " ON DELETE CASCADE;"

def process_sql(file_in, file_out, trunc):
    if os.path.isfile(file_in):
        if mimetypes.guess_type(file_in)[0] == 'application/x-sql':
            cnt = 0
            with open(file_in, 'r') as inp, open(file_out, 'w') as out:
                array = []
                for line in inp:
                    if (line.find("REFERENCES tbl_idiomas") > 0 and
                            #line.find("idioma") and
                            line.find("ON DELETE CASCADE") < 0):
                        new_line = add_ondelete(line)
                        out.write(new_line)
                        out.write("\n")
                        cnt = cnt + 1
                    elif trunc.lower() == "n" :
                        out.write(line)
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
    app_description = "Add ON DELETE CASCADE to all tables"
    parser = argparse.ArgumentParser(description=app_description)
    parser.add_argument('file_in',  help='input file')
    parser.add_argument('file_out',  help='output file')
    parser.add_argument('file_trunc', help='Show only fks modified? S/n')
    args = parser.parse_args()
    cnt_lineas = process_sql(args.file_in, args.file_out, args.file_trunc)
    print "Number of lines modified: " + str(cnt_lineas) + "."
    call(["atom", args.file_out])

if __name__ == '__main__':
    main()
