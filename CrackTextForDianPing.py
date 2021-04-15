
# 获取单个商铺名称，电话
import re
import requests
from fontTools.ttLib import TTFont

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


headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
  # 'sec-ch-ua': "'Google Chrome';v='89', 'Chromium';v='89', ';Not A Brand';v='99'",
  # 'sec-ch-ua-mobile': '?0',
  # 'Sec-Fetch-Dest': 'script',
  # 'Sec-Fetch-Mode': 'no-cors',
  # 'Sec-Fetch-Site': 'cross-site'
}

dper = input('请输入cookie中"dper"的值：')
# 'dper': 'a2a3939239ab93d52e9a02c369cd1ddf8221f5359a3a4bbfcb5b99edb03047401e8e61b43e6c5b7fc499f4412f42e4bcb801ab4fd8b9958cc4c06b8db65140e8'
cookies = {
  'dper': dper
}

while True:
  # 获取商品页面html
  # url = 'http://www.dianping.com/shop/l5pVyR84b9Z7v8VD'
  # url = 'http://www.dianping.com/shop/l9WMvQP9OzkP8UZV'
  url = input('请输入商品地址url（输入数字 0 时退出系统）：')
  if (url == '0'):
    break
  html = requests.get(url, headers=headers, cookies=cookies).text

  # 获取电话号dom
  shopName = ''.join(re.findall(r'<div class="breadcrumb">.*</a> &gt; <span>(.*?)</span> </div>', html))
  phone_ele = ''.join(re.findall(r'<p class="expand-info tel">(.*?)</p>', html)).replace('&nbsp;', ' ')

  # 获取字体加密映射关系
  num = get_font()
  # 替换phone_ele中加密的数字，文字
  for key in num:
    if key in phone_ele:
      phone_ele = phone_ele.replace(key, str(num[key]))
  
  phone_num = ''.join(re.findall(r'[0-9]+', phone_ele))
  if (len(shopName) == 0 or len(phone_num) == 0):
    print('系统异常，无法获取此商铺信息。请检查url、cookie是否正确。（如果页面出现验证码需要重启此系统）')
    if (int(input('是否继续？（1:继续 0:退出系统）：')) == 1):
      continue
    else:
      break
  print('商铺名称', shopName)
  print('联系方式', phone_num)
