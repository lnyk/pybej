#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""pybej.py

Author: William Yao <LNYK@ME.COM> at <LNYK2.COM>
Date  : 2015.05.27

A very simple script to catalyse your headsets.

USE IT UNDER YOUR OWN RISK!
"""

import sys
import getopt
import wave
import numpy as np
import scipy.signal as signal
import pyaudio
from datetime import datetime, timedelta
from time import sleep

class Locale():
    def __init__(self, lang='cn'):
        self.trans = None
        cn = {'i.1': u'中文',
              'i.2': u'英文',
        }
        en = {'i.1': 'Please choose your language',
              'i.2': 'English',
              'i.3': 'Chinese'
        }
        if lang == 'cn':
            self.trans = cn
        else:
            self.trans = en

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def CreateSweep(framerate = 44100, duration = 3, freq_start = 20, freq_stop = 18000):
    self.framerate = framerate
    self.duration = duration
    self.freq_start = freq_start
    self.freq_stop = freq_stop

    # 打开WAV文档
    f = wave.open(r"sweep.wav", "wb")

    # 配置声道数、量化位数和取样频率
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(framerate)
    # 产生升序频率扫描波
    t = np.arange(0, duration/2, 1.0/framerate)
    wave_data = signal.chirp(t, freq_start, duration/2, freq_stop, method='linear') * 10000
    wave_data = wave_data.astype(np.short)
    # 将wav_data转换为二进制数据写入文件
    f.writeframes(wave_data.tostring())
    # 产生降序频率扫描波
    wave_data = signal.chirp(t, freq_stop, duration/2, freq_start, method='linear') * 10000
    wave_data = wave_data.astype(np.short)
    # 将wav_data转换为二进制数据写入文件
    f.writeframes(wave_data.tostring())
    f.close()

def PlaySweep(
        # 开始时间
        dt_start = datetime.now(),
        # 计划用时
        dt_length = timedelta(0, 0, 0, 72, 0, 0),
        # 每隔多久休息（默认2小时）
        dt_rest_every = timedelta(0, 0, 0, 2, 0, 0),
        # 每次休息多久（默认30分钟）
        dt_rest_for = timedelta(0, 0, 0, 0, 30, 0)
):
    # 不必检查计划用时是否大于休息时间总和，过期自然退出
    chunk = 1024

    wf = wave.open(r"sweep.wav", 'rb')

    p = pyaudio.PyAudio()

    # 打开声音输出流
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # 写声音输出流进行播放

    play_count = 1
    while True:
        data = wf.readframes(chunk)
        if data == "":
            wf.rewind()
            print str(play_count)
            play_count += 1
            continue
        stream.write(data)

    stream.close()
    p.terminate()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hov:", ["help", "output="])
        except getopt.error, msg:
             raise Usage(msg)

        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(__doc__)
            if option in ("-o", "--output"):
                output = value

    except Usage, err:
        print >>sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >>sys.stderr, "	 for help use --help"
        return 2

    print Locale().trans["English"]

if __name__ == "__main__":
    sys.exit(main())
