#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""pybej.py

Author: William Yao <LNYK@ME.COM> at <LNYK2.COM>
Date  : 2015.05.27

A very simple script to catalyse your headsets.

USE IT UNDER YOUR OWN RISK!
"""

import sys
import os
import getopt
import wave
import numpy as np
import scipy.signal as signal
import pyaudio
from datetime import datetime, timedelta
from time import sleep
from translation import Locale

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def CreateSweep(framerate = 44100, duration = 3, freq_start = 20, freq_stop = 18000):
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
        # 语言类
        l,
        # 计划用时（默认24小时）
        td_length = timedelta(hours = 24),
        # 每隔多久休息（默认2小时）
        td_rest_every = timedelta(hours = 2),
        # 每次休息多久（默认30分钟）
        td_rest_for = timedelta(minutes = 30)
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

    # 定义时间变量
    dt_start = datetime.now()
    td_remain = None
    dt_next_rest = dt_start + td_rest_every
    rest_count = 0
    td_plan = td_length

    while True:
        data = wf.readframes(chunk)
        if data == "":
            print l.trans['i.11'] % (str(dt_start), str(td_length), str(td_remain))
            #print 'Play until ' + str(dt_start) + str(td_length) + ', ' + str(td_remain) + ' left.'
            wf.rewind()
            td_remain = td_length - (datetime.now() - dt_start)
            # 如果当前时刻大于下次休息时刻则进行休息
            if datetime.now() > dt_next_rest:
                td_length += td_rest_for
                dt_next_rest += td_rest_every + td_rest_for
                rest_count += 1
                print l.trans['i.12'] % (str(td_rest_for), str(dt_next_rest))
                sleep(td_rest_for.total_seconds())
            # 如果剩余时间小于0，则结束
            if td_remain < timedelta(0, 0, 0, 0, 0, 0):
                print l.trans['i.13'] % (str(dt_start), str(datetime.now()), str(td_plan), str(td_length), str(td_rest_for * rest_count), str(rest_count))
                break
            continue
        stream.write(data)

    stream.close()
    p.terminate()
    return 0

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

    freq_start = 0
    freq_stop = 0
    duration = 0.0
    td_length = None
    td_rest_every = None
    td_rest_for = None

    # 语言选择（暂时只有中文）
    l = Locale('en')

    lang = 2
    print l.trans['i.a']
    print '\t' + l.trans['i.l1']
    print '\t' + l.trans['i.l2']
    try:
        lang = int(raw_input('Your Choise (1-2): '))
    except:
        print l.trans['e.1']
        return 1
    if lang == 1:
        print 'We are not ready for English language yet! Please choose Chinese!'
        return 1
    elif lang == 2:
        l = Locale('zh_CN')
    else:
        l = Locale('zh_CN')

    # 欢迎信息
    print l.trans['i.1']
    try:
        freq_start = int(raw_input(l.trans['i.2'].encode('utf-8')))
        if freq_start < 10:
            print l.trans['e.2']
        freq_stop = int(raw_input(l.trans['i.3'].encode('utf-8')))
        if freq_stop > 22000:
            print l.trans['e.3']
        duration = float(raw_input(l.trans['i.4'].encode('utf-8')))
        (hours, minutes, seconds) = input(l.trans['i.5'].encode('utf-8'))
        td_length = timedelta(hours = hours, minutes = minutes, seconds = seconds)
        (hours, minutes, seconds) = input(l.trans['i.6'].encode('utf-8'))
        td_rest_every = timedelta(hours = hours, minutes = minutes, seconds = seconds)
        (hours, minutes, seconds) = input(l.trans['i.7'].encode('utf-8'))
        td_rest_for = timedelta(hours = hours, minutes = minutes, seconds = seconds)
    except:
        print l.trans['e.1']
        return 1
    print '=' * 15 + '\n' + l.trans['i.8'] % (str(freq_start), str(freq_stop), str(duration), str(td_length), str(td_rest_every), str(td_rest_for))

    print l.trans['i.9']
    raw_input(u'按回车键继续...'.encode('utf-8'))
    print l.trans['i.10']
    raw_input(u'按回车键继续...'.encode('utf-8'))

    CreateSweep(duration = duration, freq_start = freq_start, freq_stop = freq_stop)
    PlaySweep(l, td_length = td_length, td_rest_every = td_rest_every, td_rest_for = td_rest_for)
    if os.path.exists('sweep.wav'): os.remove('sweep.wav')
    print l.trans['i.14']
    print l.trans['i.15']

if __name__ == "__main__":
    sys.exit(main())
