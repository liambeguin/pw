#!/usr/bin/python

import os
from subprocess import call
from time import time
import numpy as np


def time_command(desc, cmd, count=10, mode='short'):
    command = cmd.split()
    t = []
    s = time()
    with open(os.devnull, 'w') as null:
        for i in range(0, 10):
            start = time()
            call(command, stdout=null, stderr=null)
            end = time()
            t.append(end - start)
    e = time() - s

    if mode == 'short':
        print("{desc} {avg:0.3}s ({dev:0.3})".format(desc=desc.ljust(50, '.'),
                                                     avg=np.average(t),
                                                     dev=np.std(t)))
    else:
        print("total time  : {:0.5} seconds".format(e))
        print("average     : {:0.5} seconds".format(np.average(t)))
        print("std dev     : {:0.5}".format(np.std(t)))
        print("variance    : {:0.5}".format(np.var(t)))
        print("count       : {}".format(len(t)))
