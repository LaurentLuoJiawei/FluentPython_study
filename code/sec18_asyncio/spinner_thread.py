"""
    Des：python asyncio_18 线程实现
    Date: 2021.05.17
"""

# 线程实现
import os
import sys
import time
import threading
from itertools import cycle


class Singal:
    done = False


def thinking():
    time.sleep(3)
    return 42

def print_think(msg, singal):
    for i in cycle('- \ | / '):
        status = i + " " + msg
        sys.stdout.write(status)
        sys.stdout.flush()
        sys.stdout.write('\x08'* len(status))
        time.sleep(.2)
        if singal.done == True:
            break
    sys.stdout.write(' '* len(status) + '\x08'*len(status))

def supervisor():
    singal = Singal()
    threading.Thread()
    spinner = threading.Thread(target=print_think, args=('thinking',singal))
    print("spinner obj", spinner)
    spinner.start()
    result = thinking()
    singal.done = True
    spinner.join()
    return result


if __name__ == '__main__':
    result = supervisor()
    print("Answer =", result)




