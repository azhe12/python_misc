#!/usr/bin/python
#coding=utf-8
from util import *
import sys, re
class Handler:
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name)
        if callable(method):
            return method(*args)
        else:
            return None

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result:
                return result
            else:
                return match.group(0)

        return substitution
    #调用如start_emphisis, start_heading
    def start(self, name):
        self.callback('start_', name)

    #调用如end_emphisis, end_heading
    def end(self, name):
        self.callback('end_', name)

class HtmlRender(Handler):
    def start_document(self):
        print '<html><head><title>...</title></head><body>'
    def end_document(self):
        print '</body><html>'

    def start_paragraph(self):
        print '<p>'
    def end_paragraph(self):
        print '</p>'

    def start_title(self):
        print '<h1>'
    def end_title(self):
        print '</h1>'

    def start_heading(self):
        print '<h2>'
    def end_heading(self):
        print '</h2>'

    def start_listitem(self):
        print '<li>'
    def end_listitem(self):
        print '</li>'

    def start_list(self):
        print '<ul>'
    def end_list(self):
        print '</ul>'

    def start_emphisis(self):
        print '<em>'
    def end_emphisis(self):
        print '</em>'

    def sub_emphisis(self, match):
        return '<em>%s</em>' %  match.group(1)

    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self, data):
        print data
#html_handler = HtmlRender()

#print re.sub(r'\*(.*)\*', html_handler.sub('em'), '*azhe*')
