import multiprocessing as mp
import numpy as np
import os, time


def task():
    print('hello world')
    time.sleep(5)

if __name__ == '__main__':
    p1 = mp.Process(target=task)
    p1.start()
    if p1.is_alive():
        print('aaaa  live')
    p1.join()
    if not p1.is_alive():
        print('aaaa still live')
    p1.terminate()
    if not p1.is_alive():
        print('yi live?')