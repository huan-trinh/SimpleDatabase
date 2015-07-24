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

class SimpleDatabase():
    def __init__(self):
        self.__database = {}
        self.__count_key = {}
        self.__recovery_log = []
        self.__current_time = 0
    def __del__(self):
        self.__database.clear()
        self.__count_key.clear()
        self.__recovery_log.clear()
    def __str__(self):
        return "Simple Database"
    def set(self, k, v):
        if k in self.__database:
            old_val = self.__database[k]
            self.__count_key[old_val] -= 1
            # add (k,v) to recovery log for possible rollback later
            self.__recovery_log.append((self.__current_time-1,k,old_val))
        self.__database[k] = v
        cnt = 1
        if v in self.__count_key:
            cnt = self.__count_key[v] + 1
        self.__count_key[v] = cnt
    def get(self, k):
        if k in self.__database:
            return self.__database[k]
        else:
            return "NULL"
    def unset(self, k):
        if k in self.__database:
            v = self.__database[k]
            # add to recovery log for possible rollback later
            self.__recovery_log.append((self.__current_time-1,k,v))
            self.__count_key[v] -= 1
            self.__database.pop(k,None)
    def numEqualTo(self, v):
        if v in self.__count_key:
            return self.__count_key[v]
        else:
            return 0
    def begin(self):
        self.__current_time += 1
    def commit(self):
        self.__recovery_log.clear()
        self.__current_time = 0
    def rollback(self):
        self.__current_time -= 1
        if len(self.__recovery_log) == 0 and self.__current_time == 0:
            self.__database.clear()
            self.__count_key.clear()
        else:
            while len(self.__recovery_log) > 0:
                (t,k,v) = self.__recovery_log[-1]
                if t != self.__current_time:
                    break
                if k in self.__database:
                    old_val = self.__database[k]
                    self.__count_key[old_val] -= 1
                self.__database[k] = v
                self.__count_key[v] += 1
                del self.__recovery_log[-1]
    def haveTrans(self):
        return True if self.__current_time > 0 else False

def start_transaction(sdb):
    while True:
        try:
            line = input()
            if line.startswith("SET"):
                (k,v) = line.split()[-2:]
                sdb.set(k,v)
            elif line.startswith("GET"):
                k = line.split()[1]
                print(sdb.get(k))
            elif line.startswith("UNSET"):
                k = line.split()[1]
                sdb.unset(k)
            elif line.startswith("NUMEQUALTO"):
                v = line.split()[1]
                print(sdb.numEqualTo(v))
            elif line == "BEGIN":
                sdb.begin()
            elif line == "COMMIT":
                if not sdb.haveTrans():
                    print("NO TRANSACTION")
                else:
                    sdb.commit()
            elif line == "ROLLBACK":
                if not sdb.haveTrans():
                    print("NO TRANSACTION")
                else:
                    sdb.rollback()
            elif line == "END":
                sys.exit(0)
        except EOFError:
            sys.exit(0)

if __name__ == '__main__':
    sdb = SimpleDatabase()
    start_transaction(sdb)
