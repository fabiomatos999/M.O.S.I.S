"""Search query parsing module."""
import re
from query import getFirstMediaEntry, getLastMediaEntry
from routes import db

dualEndedRangeRegex = r'^\d+-\d+$'
leftEndedRangeragex = r'^\d+-$'
rightEndedRangeRegex = r'-\d+$'

def parseIdRange(searchQuery: str) -> [int]:
    left = int()
    right = int()
    dbMin = getFirstMediaEntry(db)
    dbMax = getLastMediaEntry(db)
    if bool(re.search(dualEndedRangeRegex, searchQuery)):
        left = int(searchQuery.split('-')[0])
        right = int(searchQuery.split('-')[-1])
    elif bool(re.search(leftEndedRangeragex, searchQuery)):
        left = int(searchQuery.split('-')[0])
        right = dbMax
    elif bool(re.search(rightEndedRangeRegex, searchQuery)):
        left = dbMin
        right = int(searchQuery.split('-')[-1])
    else:
        left = dbMin
        right = dbMax
    if left > right:
        temp = left
        left = right
        right = temp
    if left < dbMin:
        left = dbMin
    if right > dbMax:
        right = dbMax
    return list(range(left, right+1, 1))
