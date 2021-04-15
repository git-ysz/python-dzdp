import telnetlib
# http://www.66ip.cn/index.html
try:
	telnetlib.Telnet('167.179.85.238', port='8118', timeout=3)
except:
	print('ip无效！')
else:
	print('ip有效！')
