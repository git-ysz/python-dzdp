# 获取多个商铺名称，电话
'''
pip install requests
pip install fontTools
pip install easyxlsx
'''
import re
import requests
from fontTools.ttLib import TTFont
from easyxlsx import SimpleWriter
import time
import datetime

def get_font():
  font = TTFont('PingFangSC-Regular-num.woff')
  font_names = font.getGlyphOrder()
  # print(font_names) # 字典的 value 字体文件有哪些值 对应的值
  # print(font.getBestCmap()) # 获得对应的字符对应的值
  texts = ['', '', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
  
  font_name = {}
  for index, value in enumerate(texts):
    a = font_names[index].replace('uni', '&#x').lower() + ';'
    font_name[a] = value
  return font_name

# 代理
proxies = {
  # 'http': 'http://167.179.85.238:8118'
}

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
  'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.29 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
]

headers = {
  'User-Agent': user_agent_list[4],
  # 'sec-ch-ua': "'Google Chrome';v='89', 'Chromium';v='89', ';Not A Brand';v='99'",
  # 'sec-ch-ua-mobile': '?0',
  # 'Sec-Fetch-Dest': 'script',
  # 'Sec-Fetch-Mode': 'no-cors',
  # 'Sec-Fetch-Site': 'cross-site'
}

dper = input('请输入cookie中"dper"的值：')
# dper = 'a2a3939239ab93d52e9a02c369cd1ddfd1ff5c6cc129cd1a488b84028cba9f2e0c36a1d1e72f95a93c2fc982aed57e4f94e2bbb0f32ebcf0926a8f2b1e30d27cc913bab4cc7574487559262bd070f69a40db9c3ad99de9b3a44e9ed2d3dcdcbe'

cookies = {
  'dper': dper
}

# shop_list_url = 'http://www.dianping.com/beijing/ch10'
# shop_list_url = 'http://www.dianping.com/wuhan/ch10/p1'
# shop_list_url = 'http://www.dianping.com/wuhan/ch10/p2'
# shop_list_url = 'http://www.dianping.com/wuhan/ch10/p3'
# shop_list_url = 'http://www.dianping.com/beijing/ch10/r2580'
# shop_list_url = 'http://www.dianping.com/beijing/ch10/r2580p1'
# shop_list_url = 'http://www.dianping.com/beijing/ch10/r2580p2'
shop_list_url = input('请输入商品列表地址url（例：http://www.dianping.com/beijing/ch10）：')

i = 1
page = int(input('请输入需要查询的页数（每页15条）：')) # 查询页数
print('商铺\t联系方式')
shop_list = []
while i <= page:
  if (shop_list_url[-4:] == 'ch10'):
    # 'http://www.dianping.com/wuhan/ch10'
    shop_list_url += '/p%s' % i
  elif (shop_list_url[-7:-1] == 'ch10/p'):
    # 'http://www.dianping.com/wuhan/ch10/p1'
    # 'http://www.dianping.com/wuhan/ch10/p2'
    # 'http://www.dianping.com/wuhan/ch10/p3'
    shop_list_url = shop_list_url[:-1] + str(i)
  else:
    # 'http://www.dianping.com/beijing/ch10/r2580'
    # 'http://www.dianping.com/beijing/ch10/r2580p1'
    # 'http://www.dianping.com/beijing/ch10/r2580p2'
    if (shop_list_url[-2] != 'p'):
      shop_list_url += 'p1'
    shop_list_url = shop_list_url[:-1] + str(i)
  
  try:
    # 获取商品页面html
    shop_list_html = requests.get(shop_list_url, headers=headers, cookies=cookies, proxies=proxies, timeout=5).text
  except BaseException:
    print('URL: %s 出现异常。' % shop_list_url)
    time.sleep(3)
    i += 1
    continue

  # 页面禁止访问
  if ('<div class="not-found-content">' in shop_list_html):
    print('''
      抱歉！页面无法访问......
      操作频繁，此IP已被锁定，暂时无法爬取。
      userIp：%s
      userAgent：%s
    ''' % (''.join(re.findall(r'userIp:(.*?)</p>', shop_list_html)), ''.join(re.findall(r'userAgent:(.*?)</p>', shop_list_html))))

  # 获取商铺列表dom
  shop_list_url_suffix = re.findall(r'<a onclick="LXAnalytics\(\'moduleClick\', \'shopname\'\).*?href="http://www.dianping.com/shop/(.*?)"', shop_list_html)

  font_key_value = get_font() # 获取字体加密映射关系
  for value in shop_list_url_suffix:
    shop_url = r'http://www.dianping.com/shop/%s' % value
    try:
      shop_html = requests.get(shop_url, headers=headers, cookies=cookies, proxies=proxies, timeout=5).text
    except BaseException:
      print('URL: %s 出现异常。' % shop_url)
      time.sleep(3) # 暂停3秒
      continue
    
    # 获取电话号dom
    shopName = ''.join(re.findall(r'<div class="breadcrumb">.*</a> &gt; <span>(.*?)</span> </div>', shop_html))
    phone_ele = ''.join(re.findall(r'<p class="expand-info tel">(.*?)</p>', shop_html)).replace('&nbsp;', ' ')
    
    # 替换phone_ele中加密的数字，文字
    for key in font_key_value:
      if key in phone_ele:
        phone_ele = phone_ele.replace(key, str(font_key_value[key]))
    
    phone_num = ''.join(re.findall(r'[0-9]+', phone_ele))

    # 整理联系方式，处理存在两个电话的情况
    if (len(phone_num) >= 22):
      phone_num = r'%s %s' % (phone_num[0:11], phone_num[11:])
    if (len(shopName) == 0 or len(phone_num) == 0):
      print('URL: %s 出现异常，未成功解析出商铺信息' % shop_url)
      time.sleep(3) # 暂停3秒
      continue
    else:
      shop_list.append([shopName, phone_num])
      now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      print('%s\t%s\t时间：%s' % (shopName, phone_num, now_time))
    time.sleep(3) # 暂停3秒
  
  # 继续执行下一次循环
  i += 1

# print(shops)
if (len(shop_list) > 0):
  SimpleWriter(tuple(shop_list), headers=('商铺', '联系方式'), bookname='shop.xlsx').export()
