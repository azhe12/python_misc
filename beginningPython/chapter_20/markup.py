#!/usr/bin/python
#encoding=utf-8

import sys, re
from util import  *
from handlers import *
from rules import *

class Parser:
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block):
            return re.sub(pattern, self.handler.sub(name), block)
        self.filters.append(filter)

    def parser(self, file):
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(self.handler, block)
                    if last: break  #判断是否执行余下的rule, Ture: 不执行余下action, False: 执行余下action
                
handler = HtmlRender()

parser = Parser(handler)

parser.addFilter(r'\*(.*)\*', 'emphisis')
parser.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
parser.addFilter(r'([\._a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')

parser.addRule(ListRule())
parser.addRule(ListItemRule())

parser.addRule(TitleRule())
parser.addRule(HeadingRule())
parser.addRule(ParagraphRule())

parser.parser(sys.stdin)
