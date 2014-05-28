#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

def list_file(root_dir_abs, filelist):
    for list in os.listdir(root_dir_abs):
        list = os.path.join(root_dir_abs, list)
        if os.path.isdir(list): #目录
            list_file(list, filelist)
        else:   #文件
            filelist.append(list)

'''
列出显示root_dir中的文件
'''
def list_dir(root_dir):
    if root_dir[0] != '/':  #relative dir
        root_dir = os.path.join(os.getcwd(), root_dir)

    filelist = []
    list_file(root_dir, filelist)
    return filelist

if len(sys.argv) > 1:
    print list_dir(sys.argv[1])
