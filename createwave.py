#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import wave
import numpy as np
import scipy.signal as signal
import pyaudio
from datetime import datetime, timedelta
from time import sleep

framerate = 44100
time = 1.0
freq_start = 20
freq_stop = 22000

# 产生频率扫描波
t = np.arange(0, time/2, 1.0/framerate)
wave_data = signal.chirp(t, freq_start, time/2, freq_stop, method='linear') * 10000
wave_data = wave_data.astype(np.short)
wave_data_reverse = signal.chirp(t, freq_stop, time/2, freq_start, method='linear') * 10000
wave_data_reverse = wave_data_reverse.astype(np.short)
# 打开WAV文档
f = wave.open(r"sweep.wav", "wb")

# 配置声道数、量化位数和取样频率
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(framerate)
# 将wav_data转换为二进制数据写入文件
f.writeframes(wave_data.tostring() + wave_data_reverse.tostring())
#f.writeframes(wave_data_reverse.tostring())
f.close()

chunk = 1024

wf = wave.open(r"sweep.wav", 'rb')

p = pyaudio.PyAudio()

# 打开声音输出流
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# 写声音输出流进行播放
dt_start = datetime.now()
td_length = timedelta(minutes = 1)
td_rest_every = timedelta(seconds = 10)
td_rest_for = timedelta(seconds = 5)
td_remain = None
dt_next_rest = dt_start + td_rest_every

while True:
    data = wf.readframes(chunk)
    if data == "":
        print 'Play until ' + str(dt_start) + str(td_length) + ', ' + str(td_remain) + ' left.'
        wf.rewind()
        td_remain = td_length - (datetime.now() - dt_start)
        if datetime.now() > dt_next_rest:
            print 'Resting for ' + str(td_rest_for)
            td_length += td_rest_for
            dt_next_rest += td_rest_every + td_rest_for
            sleep(td_rest_for.total_seconds())
        if td_remain < timedelta(0, 0, 0, 0, 0, 0):
            print 'Done!'
            break
        continue
    stream.write(data)

stream.close()
p.terminate()
