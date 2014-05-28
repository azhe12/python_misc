#!/usr/bin/env python
#encoding=utf-8

#azhe
#2014/5/8

import commands
import time
import StringIO
import re
import threading

open_effect = [
        (430, 756), 
        (20,431),
        (514,441),
        ]

camera_shot = (700, 250)
close_camera = (834,382)
first_effect_x,  first_effect_y = (80, 326)
shot_num = 3    #拍2张照, 第一次取消提示消息
swipe_a = (540,326)     #swipe a到b， 表示滑动effect到下一个page
swipe_b = (180,326)
last_pos = (596, 326)   #最后一个effect位置

effect_space = 90   #相邻effect之间x相差90
page_num = 3        #共3页effect
effect_num_per_page = 7 #每个page有7个effect
remain_effect = 2   #第3页只有2个effect

tst_cnt = 0
tst_round = 0

def input_tap(pos, device):
    cmd = "adb " + "-s " + device + " shell input tap " + str(pos[0]) + " " + str(pos[1])
    #print cmd
    commands.getoutput(cmd)
    time.sleep(0.5)
        

#从a点，滑动到b
def input_swipe(pos_a, pos_b, device):
    cmd = "adb " + "-s " + device + " shell input swipe " +    \
        str(pos_a[0]) + " " + str(pos_a[1]) +  " " +\
        str(pos_b[0]) + " " + str(pos_b[1])
    commands.getoutput(cmd)


#根据effect坐标，点击effect, 并拍照
def tap_effect(effect_pos, effect_pages, device):
    #打开camera effect
    for pos in open_effect:
        input_tap(pos, device)
    #effect滑动页
    for i in range(effect_pages):
        #effect 左移1个page
        input_swipe(swipe_a, swipe_b, device)

    #选择effect
    input_tap(effect_pos, device)
    #拍照
    for i in range(shot_num):
        input_tap(camera_shot, device)  #shot

    input_tap(close_camera, device) #close camera
    input_tap(close_camera, device) #close camera

#遍历一页effect
def tap_effect_page(effect_pages, device):
    #effect_num_per_page = 7 #每个page有7个effect
    effect_space = 90   #相邻effect之间x相差90
    for i in range(effect_num_per_page):
        #移动effect坐标
        cur_x = first_effect_x + i * effect_space   #每次向右移动一个effect
        cur_y = first_effect_y
        #点击effect, 并拍照
        tap_effect((cur_x, cur_y), effect_pages, device)

#获得device list
def get_devices():
    ret,info = commands.getstatusoutput("adb devices")
    s = StringIO.StringIO(info)
    first = True
    devices = []
    for line in s.readlines():
        if first == True:
            first = False
        else:
            pat = '(.*)device'
            match = re.match(pat, line)
            #print match.group(1).strip()
            devices.append(match.group(1).strip())
    return devices

class DeviceThread(threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device

    def run(self):
        global tst_round
        print "Device: %s begin test!" % device
        while True:
            #测试前2页effect
            for effect_page in range(page_num - 1):
                tap_effect_page(effect_page, self.device)
        
            #点击余下的2个effect, 他们在第3页
            for i in range(remain_effect):
                cur_x = last_pos[0] - i * effect_space
                cur_y = last_pos[1]
                tap_effect((cur_x, cur_y), page_num - 1, self.device);
        
            tst_round += 1
            tst_effect_cnt = tst_round * ((page_num - 1)*effect_num_per_page+ remain_effect)
            commands.getoutput("adb shell rm -rf /sdcard2/DCIM/100MEDIA /sdcard/DCIM/100MEDIA")
            print "Device %s test round: %d, effects: %d" % (device, tst_round, tst_effect_cnt)



#获得设备列表
devices = get_devices()

for device in devices:
    tst_thread = DeviceThread(device)
    tst_thread.setDaemon(True)  #设置和主线程同时结束
    tst_thread.start()

while True:
    pass

