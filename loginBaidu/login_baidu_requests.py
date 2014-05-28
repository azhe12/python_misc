#!/usr/bin/env python
#encoding=utf-8
'''
模拟登录百度http://www.baidu.com
登录步骤:
    1. 访问url_baidu, 生成cookie
    2. 访问url_getApi, 获取token值
    3. 访问url_login, 最终登录

分析过程:
    1. 依据密码查找到实际的登录url_login是 https://passport.baidu.com/v2/api/?login
    2. 登录url_login的request body中最为关键，且不能直接得到的数据为 token, 因此要去查找token的由来. (有些数据可以忽略，如tt,ppui_logintime )
    3. 发现token最早来自与对 url_getApi: https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=1395130158576&class=login&logintype=dialogLogin&callback=bd__cbs__o22c1w 
        访问之后的responce body, 中得到的。因此在登录之前需要对上述url_getApi进行request 以获得token.
    4. 实际对url_getApi访问，返回的request数据为空，表示访问失败。查询原因，发现request header中有cookie信息，而这些cookie信息在，
        request url_baidu: http://www.baidu.com时会生成。因此需要首先访问url_baidu, 生成相应cookie.
'''
import urllib2
import urllib
import cookielib
import re
import argparse
import requests
import requests_cache
import json
from cookielib import LWPCookieJar

def show_cookie(CookieJar):
    for i, c in enumerate(CookieJar):
        print 'Cookie [%d]: %s = %s' % (i, c.name, c.value)

def print_delimiter():
    print '-'*80

url_baidu = 'http://www.baidu.com'
url_getApi = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=1395110168559&class=login&logintype=dialogLogin&callback=bd__cbs__1tr0a2'
url_login = 'https://passport.baidu.com/v2/api/?login'
CACHE_FILE = 'cacheLoginBaidu'

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0)'
header = {'User-Agent':user_agent}

def get_parser():
    parser = argparse.ArgumentParser(description='emulate login www.baidu.com')
    parser.add_argument('-u', '--user', help='user name of baidu', type=str)
    parser.add_argument('-p', '--password', help='password of baidu', type=str)

    return parser

def login_baidu():
    parser = get_parser()
    args = vars(parser.parse_args())
    #print 'args: ', args
    #print args
    if not args['user'] or not args['password']:
        parser.print_help()
        return

    username = args['user'] #登录名和密码
    passwd = args['password']

    requests_cache.install_cache(CACHE_FILE)

    s = requests.Session()
    
    #step 1: GET 获取cookie
    print_delimiter()
    print 'Step 1: get cookie from %s' % url_baidu

    '''
    req_baidu = requests.get(url_baidu, headers=header)
    #req_baidu = requests.get(url_baidu)
    req_baidu_cookies = req_baidu.cookies
    req_baidu_cooike_dict = requests.utils.dict_from_cookiejar(req_baidu_cookies)

    print 'cookie values:', req_baidu_cookies.values
    print 'cookie keys:', req_baidu_cookies.keys
    print 'cookie dict: ', req_baidu_cooike_dict
    #s.get(url_baidu, headers=header)
    '''
    r = s.get(url_baidu, headers=header)
    print requests.utils.dict_from_cookiejar(r.cookies)

    
    #step 2: GET 获取token
    print_delimiter()
    print 'Step 2: get token from %s' % url_getApi
    '''
    req_getApi = requests.get(url_getApi, headers=header, cookies=req_baidu_cooike_dict)
    #req_getApi = s.get(url_getApi, headers=header)

    req_text = req_getApi.text
    
    '''
    res_text = s.get(url_getApi, headers=header, cookies=s.cookies).text
    print 'responce body = \n', res_text
    pattern = '"token" : "(.*)", "cookie"'
    #pattern = 'token'
    match = re.search(pattern, res_text)
    token = match.group(1)
    print 'token = %s' % token
    print_delimiter()
    
    #step 3: 登录www.baidu.com
    print 'Step 3: login %s' % url_baidu

    #以下是request body中的数值
    staticpage_encode = 'http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fv3Jump.html'
    u_tag_encode = 'http%3A%2F%2Fwww.baidu.com%2Findex.php%3Ftn%3D98012088_4_dg'
    staticpage = urllib2.unquote(staticpage_encode) #http://www.baidu.com/cache/user/html/v3Jump.html
    u_tag = urllib2.unquote(u_tag_encode) #http://www.baidu.com/index.php?tn=98012088_4_dg 
    
    post_dict = {
            'staticpage':staticpage,
            'charset':'utf-8',
            'token':token,
            'tpl':'mn',
            'apiver':'v3',
            'tt':'1395110195915',
            'safeflg':'0',
            'u':u_tag,
            'quick_user':'0',
            'logintype':'dialogLogin',
            'logLoginType':'pc_loginDialog',
            'loginmerge':'true',
            'splogin':'rate',
            'username':username,
            'password':passwd,
            'mem_pass':'on',
            'ppui_logintime':'27356',
            'callback':'parent.bd__pcbs__jz9gqq'
            }
    
    #post_data = urllib.urlencode(post_dict) #将字典编码为http格式数据如, username=liuyuanzhe123%40126.com&password=lyz13.BAIDU&tpl=mn&mem_pass=on& 
    #print 'post_data = ', post_data
    
    
    #req = urllib2.Request(url_login, post_data, header) #使用urllib2发送POST请求
    #response = urllib2.urlopen(req)
    req_login = requests.post(url_login, params=json.dumps(post_dict), headers=header) #将post_dict转为json字符串, 然后POST
    response_login = req_login.text
    print 'response:', response_login
    

if __name__ == '__main__':
    login_baidu()
