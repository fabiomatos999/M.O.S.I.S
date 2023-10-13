"""Search query parsing module."""
import re
from query import getFirstMediaEntry, getLastMediaEntry

dualEndedRangeRegex = r'^\d+-\d+$'
leftEndedRangeragex = r'^\d+-$'
rightEndedRangeRegex = r'^-\d+$'
commaSeparatedValueRegex = r'^(\d+,)+\d+$'
singleValueRagex = r'^\d+$'


def parseIdRange(db, searchQuery: str) -> [int]:
    dbMin = getFirstMediaEntry(db)
    dbMax = getLastMediaEntry(db)
    entries = set()
    left = int()
    right = int()
    for query in searchQuery.split(" "):
        if bool(re.search(dualEndedRangeRegex, query)):
            left = int(query.split('-')[0])
            right = int(query.split('-')[-1])
            for i in returnRange(left, right, dbMin, dbMax):
                entries.add(int(i))
        elif bool(re.search(leftEndedRangeragex, query)):
            left = int(query.split('-')[0])
            right = dbMax
            for i in returnRange(left, right, dbMin, dbMax):
                entries.add(int(i))
        elif bool(re.search(rightEndedRangeRegex, query)):
            left = dbMin
            right = int(query.split('-')[-1])
            for i in returnRange(left, right, dbMin, dbMax):
                entries.add(int(i))
        elif bool(re.search(commaSeparatedValueRegex, query)):
            values = query.split(',')
            for i in values:
                entries.add(int(i))
        elif bool(re.search(singleValueRagex, query)):
            entries.add(int(query))
    entries = list(filter(lambda x: x >= dbMin and x <= dbMax, entries))
    entries.sort()
    return entries


def returnRange(left: int, right: int, dbMin: int, dbMax: int) -> [int]:
    if left > right:
        temp = left
        left = right
        right = temp
    if left < dbMin:
        left = dbMin
    if right > dbMax:
        right = dbMax
    return list(range(left, right + 1, 1))
