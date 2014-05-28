#!/usr/bin/python
#coding=utf-8
from xml.dom import minidom
import os, subprocess

config_file = "config.xml"

def get_xmlnode(father, name):
    return father.getElementsByTagName(name) if father else []

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else []

conf = minidom.parse(config_file)
#node:root
root = conf.documentElement


#node:project
nodes_projects = get_xmlnode(root, "project")
#遍历node
for node in nodes_projects:
    #name node
    element_name = "name"
    node_name = get_xmlnode(node, element_name)
    if not node_name:
        print "not find %s element" % element_name
        exit(-1)
    #resolution node
    element_name = "resolution"
    node_resolution = get_xmlnode(node, element_name)
    if not node_resolution:
        print "not find %s element" % element_name
        exit(-1)
    #width
    element_name = "width"
    node_width = get_xmlnode(node_resolution[0], element_name)
    if not node_width:
        print "not find %s element" % element_name
        exit(-1)
    #height
    element_name = "height"
    node_height = get_xmlnode(node_resolution[0], element_name)
    if not node_height:
        print "not find %s element" % element_name
        exit(-1)
    #get value
    name = get_nodevalue(node_name[0])
    width = get_nodevalue(node_width[0])
    height = get_nodevalue(node_height[0])
    print name, width, height

#os.system("ls")
#p = subprocess.Popen("ls", stdout=subprocess.PIPE)
#p = subprocess.Popen("ls")

