#-------------------------------------------------------------------------------
# Name:        simple database
# Purpose:
#
# Author:      Huan
#
# Created:     16/07/2015
# Copyright:   (c) Huan 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
from copy import deepcopy

trans = 0

def start_transaction(previous_database, previous_count_key):
    global trans
    database = deepcopy(previous_database)
    count_key = deepcopy(previous_count_key)
    while True:
        try:
            line = input()
            if line.startswith("SET"):
                (k,v) = line.split()[-2:]
                if k in database:
                    old_val = database[k]
                    count_key[old_val] -= 1
                database[k] = v
                cnt = 1
                if v in count_key:
                    cnt = count_key[v] + 1
                count_key[v] = cnt
            elif line.startswith("GET"):
                k = line.split()[1]
                if k in database:
                    print(database[k])
                else:
                    print("NULL")
            elif line.startswith("UNSET"):
                k = line.split()[1]
                if k in database:
                    count_key[database[k]] -= 1
                    database.pop(k, None)
            elif line.startswith("NUMEQUALTO"):
                v = line.split()[1]
                if v in count_key:
                    print(count_key[v])
                else:
                    print(0)
            elif line == "BEGIN":
                trans += 1
                start_transaction(database, count_key)
            elif line == "COMMIT":
                if trans == 0:
                    print("NO TRANSACTION")
                else:
                    previous_database.clear()
                    previous_count_key.clear()
                    for k in database:
                        previous_database[k] = database[k]
                    for v in count_key:
                        previous_count_key[v] = count_key[v]
                    trans = 0
                return
            elif line == "ROLLBACK":
                if trans == 0:
                    previous_database.clear()
                    previous_count_key.clear()
                    for k in database:
                        previous_database[k] = database[k]
                    for v in count_key:
                        previous_count_key[v] = count_key[v]

                    print("NO TRANSACTION")
                else:
                    return
            elif line == "END":
                sys.exit(0)
        except EOFError:
            sys.exit(0)

if __name__ == '__main__':
    start_transaction({},{})
