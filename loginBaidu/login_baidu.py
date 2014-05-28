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

def show_cookie(CookieJar):
    for i, c in enumerate(CookieJar):
        print 'Cookie [%d]: %s = %s' % (i, c.name, c.value)

def print_delimiter():
    print '-'*80

url_baidu = 'http://www.baidu.com'
url_getApi = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=1395110168559&class=login&logintype=dialogLogin&callback=bd__cbs__1tr0a2'
url_login = 'https://passport.baidu.com/v2/api/?login'

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

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    
    urllib2.install_opener(opener)
    
    #step 1: 获取cookie
    print_delimiter()
    print 'Step 1: get cookie from %s' % url_baidu
    res_baidu = urllib2.urlopen(url_baidu)
    show_cookie(cj)
    
    
    #step 2: 获取token, 如果没有step1, 那么token = the fisrt two args should be string type:0,1!
    print_delimiter()
    print 'Step 2: get token from %s' % url_getApi
    
    res_getApi = urllib2.urlopen(url_getApi)
    
    res_str = res_getApi.read()
    print 'responce body = \n', res_str
    
    pattern = '"token" : "(.*)", "cookie"'
    #pattern = 'token'
    match = re.search(pattern, res_str)
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
    
    post_data = urllib.urlencode(post_dict) #将字典编码为http格式数据如, username=xxx&password=xxxx&tpl=mn&mem_pass=on& 
    print 'post_data = ', post_data
    
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0)'
    
    header = {'User-Agent':user_agent}
    
    req = urllib2.Request(url_login, post_data, header) #使用urllib2发送POST请求
    response = urllib2.urlopen(req)
    
    #print response.read()
    show_cookie(cj)

if __name__ == '__main__':
    login_baidu()
