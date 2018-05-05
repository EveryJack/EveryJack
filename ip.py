#原作者 https://github.com/q1271964185
#修改2018/5/5 某人
# coding: utf-8
import requests
from bs4 import BeautifulSoup

header = {
    'Host': 'www.xicidaili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'http://www.xicidaili.com/api',
    'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWY4OWQyNjM2Nzg1NTE4M2IyOWVhMmUxMzA3MzVjNjZmBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXlkTzEzeU0zMHNzZnpzdFNMUjBuYlpQcXBiVG11Z1orOGgxVUl1MUlBSU09BjsARg%3D%3D--36c753329ee7efae052302d32a239d8d848f2642',
    'Connection': 'close',
    'Upgrade-Insecure-Requests': '1',
    'If-None-Match': 'W/"f23ff6cb48ac17d32c5071dca24dcead"',
    'Cache-Control': 'max-age=0'
}

''''' 
获取所有代理IP地址,并调用函数进行可用性测试，再调用函数将可用的写入数据库
'''
def getProxyIp(header):
    for x in range(1,2):#这里自行根据需要改变
        url = "http://www.xicidaili.com/nn/{0}".format(x)
        html = requests.get(url=url,headers=header).text
        soup = BeautifulSoup(html,"html.parser")
        ips = soup.findAll('tr')
        num = 0
        for x in range(1, len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]#ip
            protocal = tds[5].contents[0]#协议
            try:
                place = tds[3].find('a').contents[0]  # 服务器地址
            except:
                place = '空'
            value = validateIp(ip_temp,protocal)
            if(value == True):
                WriteMysql(ip_temp,place,protocal)
                num = num +1
            elif(value == False):
                pass
            else:
                print("IP："+ip_temp+'出现异常问题')
    return num

''''' 
将可用代理ip写入数据库
'''
def WriteMysql(ip,place,protocal):
    f = open('OKIP.txt','a')
    str = ip+"  "+place+"  "+protocal+"\n"
    f.write(str)
    f.close()

''''' 
验证获得的代理IP地址是否可用 
'''
def validateIp(ip,protocol):
    url = "http://xx.xxxxx.com/"#查ip
    try:
        proxy_host = {protocol:protocol+"://"+ip}
        html = requests.get(url,proxies = proxy_host,timeout=3) #
        if(html.status_code == 200):
            data = html.text
            ip1 = ip.split(':')
            print(data)
            if(ip1[0] in data):
                return True
             #将IP改为你的IP
            elif ("127.0.0.1" in data):
                return True
            else:
                return False
        else:
            return False
    except:
        return 'error'

if __name__ == '__main__':
    num = getProxyIp(header)
    print("本次成功入库有效代理IP"+str(num)+"条")
