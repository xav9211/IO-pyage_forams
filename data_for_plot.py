#!/usr/bin/env python
# coding=utf-8
import sys
import csv

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)
    result = ''
    for row in reader:
        result += row[0] + ' ' + row[1] + ' ' + row[3] + '\n'
    with open('result.txt', 'wb') as resultfile:
        resultfile.write(result)