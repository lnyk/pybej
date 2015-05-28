#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""pybej.py

Author: William Yao <LNYK@ME.COM> at <LNYK2.COM>
Date  : 2015.05.27

A very simple script to catalyse your headsets.

USE IT UNDER YOUR OWN RISK!
"""
class Locale():
    def __init__(self, lang='en'):
        self.trans = None
        zh_CN = {'i.1': u'欢迎使用 pybej 煲耳机小程序！\n\n注意：不适当的煲耳机过程有可能会损坏您的设备，请谨慎使用！\n',
                 'i.2': u'扫频的起始频率（例如 100）：',
                 'i.3': u'扫频的终止频率（例如 15000）：',
                 'i.4': u'扫频的单次循环时长（单位秒，例如 5）：',
                 'i.5': u'此次任务的计划用时（格式：时,分,秒 例如 72,0,0）：',
                 'i.6': u'自动休息每隔（格式：时,分,秒 例如 2,0,0）：',
                 'i.7': u'每次休息时长（格式：时,分,秒 例如 0,30,0）：',
                 'i.8': u'本次计划如下\n\n扫频范围：%s - %s\n扫频时长：%s\n计划用时：%s\n每隔 %s 自动休息\n每次休息 %s\n',
                 'i.9': u'以上为本次计划内容，请确认内容并按回车键继续！\n如需放弃，请按 Ctrl+C 或直接关闭窗口！\n',
                 'i.10': u'扫频任务即将开始，请将输出设备音量调至最低。\n按回车键，等待扫频开始后逐渐增大音量至所需位置！\n扫频期间按 Ctrl+C 退出，或直接关闭窗口。\n',
                 'i.11': u'[开始时间 %s][计划用时 %s][剩余时间 %s]\n',
                 'i.12': u'[自动休息 %s][预计于 %s 自动恢复扫频]\n',
                 'i.13': u'任务完成！\n本次任务\n开始于 %s\n结束于 %s\n计划用时 %s\n实际用时 %s\n其中包含休息用时 %s\n共休息 %s 次\n',
                 'i.14': u'临时文件清理完毕！\n',
                 'i.15': u'欢迎访问 http://blog.lnyk2.com 了解更新内容！\n\n再次感谢您对 pybej 煲耳机小程序的支持！\n软件就应开源！',
                 'e.1': u'输入有误，请检查输入内容是否符合要求！\n',
                 'e.2': u'请注意，频率设置可能过低！建议不要低于 15！',
                 'e.3': u'请注意，频率设置可能过高！建议不要高于 22000',
        }
        en = {'i.a': 'Please choose your language: \n',
              'i.l1': '1. English\n',
              'i.l2': u'2. 简体中文\n',
              'e.1': 'Input error! Please check your input again!\n',
        }
        if lang == 'zh_CN':
            self.trans = zh_CN
        elif lang == 'en':
            self.trans = en
