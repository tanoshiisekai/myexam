import hashlib
import moment
import random


def getrandomanswer():
    answer = ""
    if random.random() >= 0.5:
        answer = answer + 'A'
    if random.random() >= 0.5:
        answer = answer + 'B'
    if random.random() >= 0.5:
        answer = answer + 'C'
    if random.random() >= 0.5:
        answer = answer + 'D'
    return answer


def getsecretstr(msg, key):
    m = hashlib.md5()
    m.update((msg+key).encode("utf-8"))
    secret = m.hexdigest()
    return secret


def getnowtimestr():
    return moment.now().strftime("%Y-%m-%d %H:%M:%S")