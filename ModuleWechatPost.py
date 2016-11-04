# -*- coding: UTF-8 -*-
import requests
from pyquery import PyQuery as pq


import logging

import time

import httplib
import mimetypes

headers = {'Referer': 'http://weixin.join-inedu.com/core/login.php?', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Host': 'weixin.join-inedu.com', 'Origin': 'http://weixin.join-inedu.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'}


def getCookieAndUrl(usr, psswd):

    session = requests.Session()

    payload = {'name': usr, 'pass': psswd}
    session.post('http://weixin.join-inedu.com/core/login.php',
                 headers=headers, data=payload)

    getUrl = requests.get('http://weixin.join-inedu.com/core/info_list.php?class_id=103102', cookies=session.cookies)
    d = pq(getUrl.text)
    id = int(d('.listTable .listTr a').attr('href').split('=')[-1])
    targetUrl = 'http://weixin.join-inedu.com/core/' + '='.join(d('.listTable .listTr a').attr('href').split('=')[0:-1]) + '=%d' % id
    return targetUrl, session.cookies


def encode_multipart_formdata(fields, cookie):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    print type(fields)
    BOUNDARY = '----WebKitFormBoundary%s' % cookie['PHPSESSID']
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    # for (key, filename, value) in files:
    #     L.append('--' + BOUNDARY)
    #     L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
    #     L.append('Content-Type: %s' % get_content_type(filename))
    #     L.append('')
    #     L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def postWecourse(usr, psswd, class_id, title, content):

    url, cookie = getCookieAndUrl(usr, psswd)
    h, m = encode_multipart_formdata([('data[sortnum]', '30'), ('data[state]', '1'), ('data[class_id]', class_id),
                                      ('data[views]', '1'), ('data[content]', content),
                                      ('data[title]', title), ('data[createdTime]', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))], cookie)
    headers['Content-Type'] = h

    r = requests.post(targetUrl, cookies=session.cookies, headers=headers, data=m).content
    return r.status_code
