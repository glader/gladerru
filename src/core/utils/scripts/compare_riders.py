import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.path.dirname(__file__), '../../../')))

import settings

from django.core.management import setup_environ
setup_environ(settings)
from core.models import Man


def levenshtein_distance(first, second):
    """Find the Levenshtein distance between two strings."""
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for _ in range(first_length)]
    for i in range(first_length):
        distance_matrix[i][0] = i
    for j in range(second_length):
        distance_matrix[0][j] = j
    for i in xrange(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j - 1] + 1
            substitution = distance_matrix[i - 1][j - 1]
            if first[i - 1] != second[j - 1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length - 1][second_length - 1]

people = list(Man.objects.all())
checks = []

for i, man in enumerate(people):
    for man2 in people:
        if man.pk >= man2.pk:
            continue

        checks.append((man, man2, levenshtein_distance(man.title, man2.title), levenshtein_distance(man.slug, man2.slug)))
        print chr(13), i,

checks.sort(key=lambda x: x[2])

res = open('compare', 'w')
for row in checks:
    res.write("\t".join((str(row[0].pk), str(row[1].pk), str(row[2]), str(row[3]))))
    res.write("\n")
res.close()

print checks[:20]
