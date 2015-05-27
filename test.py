#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread

import datetime

dt1 = datetime.datetime.now()
print dt1
dt2 = datetime.datetime(2015,5,27,21,51,00)
print dt2

dt3 = datetime.timedelta(0,0,0,0,1,0)
print dt3

if dt1 - dt2 > dt3:
    print "OK"
