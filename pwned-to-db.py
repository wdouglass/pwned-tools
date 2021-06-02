#!/usr/bin/env python3
#
# @file pwned-to-db.py
#
# A script to convert haveibeenpwned password databases to sqlite
#


def main():
    from optparse import OptionParser
    import sys
    import sqlite3

    parser = OptionParser()
    parser.add_option("-i", "--in", dest="infile")
    parser.add_option("-o", "--out", dest="outfile")
    options, args = parser.parse_args(sys.argv)
    with sqlite3.connect(options.outfile) as con:
        cur = con.executescript("pragma synchronous=off; create table pw (hash NVARCHAR[32] PRIMARY KEY, count INTEGER NOT NULL);")
        cnt = 0
        with open(options.infile, "r") as i:
            insert_list = []
            for l in i:
                h = l.split(":")
                insert_list.append((h[0], int(h[1].strip())))
                print(".", end="", flush=True);
                if (cnt % 2000 == 0):

                    cur.executemany("insert into \"pw\" VALUES(?, ?)", insert_list)
                    insert_list = []
                    con.commit();

            cur.executemany("insert into \"pw\" VALUES(?, ?)", insert_list)
            con.commit();

if __name__ == "__main__":
    main()
