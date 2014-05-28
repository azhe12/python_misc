#!/usr/bin/env python
#encoding=utf-8

from pprint import pprint
import requests
import sys
import random
import os
from pyquery import PyQuery as pq
from time import clock
from urllib import urlretrieve

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)

img_cnt = 0

#TODO:设置代理， 参考howdoi
def get_proxies():
    pass


#获取url的html文本
def get_results(url):
    return requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_proxies()).text


#获取url的图片并保存在path
def get_img_links(html):
    #f = open("test.html", 'wb+')
    #f.write(get_results(url))
    #f.close()

    result = pq(html)
    #在id='article_content'且class='article_content'的节点中查找所有的标签<a>, 这些<a>标签的href属性内容生成一个列表
    #此处仅仅for CNDN blog
    links = [a.attrib['src'] for a in result('#article_content.article_content')('img')]
    pprint(links)
    return links

def get_url_title(html):
    result = pq(html)
    return result('.article_title')('a').text()



def save_picture(url):
    global img_cnt
    html = get_results(url)
    links = get_img_links(html)
    title = get_url_title(html)

    save_img_dir = os.getcwd() + '/' + title #图片保存目录
    print save_img_dir
    os.mkdir(save_img_dir)
    for link in links:
        img_name = str(img_cnt) + '.png'
        img_cnt = img_cnt + 1
        urlretrieve(link, save_img_dir + '/' + img_name)

def main(url):
    save_picture(url)


if __name__ == '__main__':
    start = clock()
    main(sys.argv[1])
    end = clock()
    print 'time elapse: ' + str((end - start)/1000000) + 's'
