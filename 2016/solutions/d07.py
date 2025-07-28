from io import TextIOWrapper
from dataclasses import dataclass
import re


def abba(string: str) -> bool:
    for i in range(len(string)-3):
        if string[i] == string[i+3] and string[i+1] == string[i+2] and string[i] != string[i+1]:
            return True
    return False


def aba(string: str) -> bool:
    patterns = set()
    for i in range(len(string)-2):
        if string[i] == string[i+2] and string[i+1] != string[i+2]:
            patterns.add(string[i:i+3])
    return patterns


def main(file: TextIOWrapper):
    ips = [line.strip() for line in file.readlines()]
    abba_count = 0
    aba_count = 0
    for ip in ips:
        found = False
        parts = re.split(r'\]|\[', ip)
        for i, part in enumerate(parts):
            if i%2 == 0 and abba(part):
                found = True
            elif abba(part):
                found = False
                break
        abba_count += found

        non_bracket_aba = set()
        bracket_aba = set()
        for i, part in enumerate(parts):
            if i%2 == 0:
                non_bracket_aba |= aba(part)
            else:
                bracket_aba |= aba(part)
        found_aba = False
        for outside in bracket_aba:
            for inside in non_bracket_aba:
                if outside[0] == inside[1] and inside[0] == outside[1]:
                    aba_count += 1
                    found_aba = True
                    break
            if found_aba:
                break

    return abba_count,aba_count
