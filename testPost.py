import requests
from pyquery import PyQuery as pq

form = dict()
session = requests.Session()

payload = {'name': 'admin', 'pass': 'admin777'}
headers = {'Referer': 'http://weixin.join-inedu.com/core/login.php?', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Host': 'weixin.join-inedu.com', 'Origin': 'http://weixin.join-inedu.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'}
r = session.post('http://weixin.join-inedu.com/core/login.php',
                 headers=headers, data=payload)

r2 = requests.get('http://weixin.join-inedu.com/core/info_list.php?class_id=103102', cookies=session.cookies)
d = pq(r2.text)
id = int(d('.listTable .listTr a').attr('href').split('=')[-1]) + 1
targetUrl = 'http://weixin.join-inedu.com/core/' + '='.join(d('.listTable .listTr a').attr('href').split('=')[0:-1]) + '=%d' % id
print targetUrl
r3 = requests.get(targetUrl, cookies=session.cookies)
r4 = requests.get('http://weixin.join-inedu.com/core/main.php', cookies=session.cookies)
headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundary%s' % session.cookies['PHPSESSID']
imgload = {'localUrl': (None, '/home/dun/Downloads/images.jpg'), 'imgFile': open('/home/dun/Downloads/images.jpg', 'rb')}
r5 = requests.post('http://weixin.join-inedu.com/core/kindeditor/php/upload_json.php?dir=image', headers=headers, cookies=session.cookies, files=imgload)

print r5.content
