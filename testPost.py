import requests

form = dict()
session = requests.Session()

payload = {'name': 'admin', 'pass': 'admin777'}
headers = {'Referer':'http://weixin.join-inedu.com/core/login.php?','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Host': 'weixin.join-inedu.com', 'Origin': 'http://weixin.join-inedu.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'}
r = session.post('http://weixin.join-inedu.com/core/login.php',
                  headers=headers, data=payload)
print session.cookies.get_dict()['PHPSESSID']
# r = requests.post("http://weixin.join-inedu.com/core/info_edit.php?class_id=103102&select_class=103102&select_state=0&keyword=&page=1")
