# -*- coding: UTF-8 -*-
import requests
from pyquery import PyQuery as pq

from requests_toolbelt import MultipartEncoder

import logging

form = dict()
session = requests.Session()

payload = {'name': 'admin', 'pass': 'admin777'}
headers = {'Referer': 'http://weixin.join-inedu.com/core/login.php?', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Host': 'weixin.join-inedu.com', 'Origin': 'http://weixin.join-inedu.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'}
r = session.post('http://weixin.join-inedu.com/core/login.php',
                 headers=headers, data=payload)

r2 = requests.get('http://weixin.join-inedu.com/core/info_list.php?class_id=103102', cookies=session.cookies)
d = pq(r2.text)
id = int(d('.listTable .listTr a').attr('href').split('=')[-1])
targetUrl = 'http://weixin.join-inedu.com/core/' + '='.join(d('.listTable .listTr a').attr('href').split('=')[0:-1]) + '=%d' % id
print targetUrl
r3 = requests.get(targetUrl, cookies=session.cookies)
r4 = requests.get('http://weixin.join-inedu.com/core/main.php', cookies=session.cookies)
content = """
<p class="MsoListParagraph" style="margin-left:24.0pt;text-indent:-24.0pt;">
	引导学生回顾<span>Arduino</span>的使用方法，学习图形化编程的基本知识。
</p>
<p class="MsoTitle">
	第一步：编写程序，让小车前进或后退
</p>
<p class="MsoTitle">
	第二步：编写程序，让小车差速转弯<span></span> 
</p>
<p class="MsoListParagraph" style="margin-left:24.0pt;text-indent:-24.0pt;">
	分别尝试让小车原地转弯、绕一侧轮子转弯和正常差速转弯。
</p>
<p class="MsoNormal">
	<span style="line-height:1.5;">第三步：使用</span><span style="line-height:1.5;">if</span><span style="line-height:1.5;">语句，让小车到达黑线即停止</span><br />
正常差速转弯：<span></span> 
</p>
<p class="MsoTitle">
	<span></span> 
</p>
<p class="MsoListParagraph" style="margin-left:24.0pt;text-indent:-24.0pt;">
	在地上用黑胶布设置一条黑线，编写程序，要求小车前端检测到黑线就停。要实现此功能，逻辑上的关系为——<span>if</span>：<span>A0</span>数值大于<span>400</span>（黑线数值为<span>450</span>左右，这里可以取小一些）或<span>A7</span>数值大于<span>400</span>——马达停转；<span>else</span>——左右马达正转，且转速相同；无限循环。<span></span> 
</p>
<h3>
	<br />
</h3>

"""
load2 = {'data': (None, {'sortnum': (None, '30'), 'state': (None, '1'), 'class_id': '103102118',
                         'views': (None, '1'), 'content': (None, content), 'title': (None, '涵乐园创客启蒙班')})}
load = {'data[sortnum]': (None, '30'), 'data[state]': (None, '1'), 'data[class_id]': '103102118',
        'data[views]': (None, '1'), 'data[content]': (None, content), 'data[title]': (None, '涵乐园创客启蒙班')}

m = MultipartEncoder(fields={'sortnum': '30', 'state': '1', 'class_id': '103102118',
                             'views': '1', 'content': content, 'title': u'涵乐园创客启蒙班'})
headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundary%s' % session.cookies['PHPSESSID']
# headers['Content-Type'] = m.content_type
r5 = requests.post(targetUrl, cookies=session.cookies, headers=headers, data=m)
# print session.cookies['PHPSESSID']
print r5.request.headers
print r5.content
