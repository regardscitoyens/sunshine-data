from pprint import pprint as pp
import csv

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def info(string):
    print colorize(string, colors.OKBLUE)

def warn(string):
    print colorize(string, colors.WARNING)

def colorize(string, color):
    return color + string + colors.ENDC

def save(string, path):
    with open(path,"w") as f:
        f.write(string)

def save_csv(table, path):
    with open(path, 'wb') as csvfile:
        w = csv.writer(csvfile)
        for row in table:
            w.writerow([l.encode('utf-8') for l in row])

def table(table):
    for l in table:
        for el in l:
            print el,
        print
