#!/usr/bin/env python


import sys
import random
from datetime import datetime, timedelta


time_format = "%Y-%m-%d %H:%M:%S"
time_start = datetime.strptime("2018-04-13 16:35:21", time_format)


random.seed(datetime.now())


while True:
    line = sys.stdin.readline()
    if not line:
        break
    time_start = time_start + timedelta(0, random.randint(0, 5))
    print "%s;%s" % (datetime.strftime(time_start, time_format), line),
