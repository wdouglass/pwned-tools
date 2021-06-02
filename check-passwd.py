#!/usr/bin/env python3
#
# @file check-passwd.py
#
# Check a password against a sql database
#

def ntlmhash(instr):
    import hashlib
    in16le = instr.encode('utf-16le')
    hobj = hashlib.new('md4', in16le)
    return hobj.hexdigest().upper()

if __name__ == "__main__":
    import getpass
    import sqlite3
    import sys
    from optparse import OptionParser
    pw = getpass.getpass()
    hpw = ntlmhash(pw)


    parser = OptionParser()
    parser.add_option("-d", "--db", dest="db")
    options, args = parser.parse_args(sys.argv)

    with sqlite3.connect(options.db) as con:
        cur = con.execute("select count from pw where hash == ?", (hpw,))
        row = cur.fetchone();
        if row:
            print(f"The password is leaked {row[0]} times");
        else:
            print("This password is not in the database")
