'''
Author: galeliu
Date: 2024-07-30 11:04:48
LastEditTime: 2024-07-30 11:09:03
LastEditors: galeliu
Description: .
'''
# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
from bs4 import BeautifulSoup
import requests
import random


def get_ipInfors(url, headers):
    '''
    爬取IP数据,单个IP信息以json格式存储，所有json格式的IP数据信息放入列表中
    return：ip_infor
    '''
    # 设置最大重定向次数为50
    session = requests.Session()
    session.max_redirects = 50
    web_data = session.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    nodes = soup.find_all('tr')

    for node in nodes[1:]:
        ip_ = node.find_all('td')
        ip_address = ip_[1].text
        ip_port = ip_[2].text
        ip_type = ip_[5].text
        ip_time = ip_[8].text

    ip_infors = {
        "ip_address": ip_address,
        "ip_port": ip_port,
        "ip_type": ip_type,
        "ip_time": ip_time
    }
    return ip_infors


def write_ipInfors(ip_infors):
    '''
    将IP数据写入文件中
    '''
    for ip_infor in ip_infors:
        f = open('IP.txt', 'a+', encoding='utf-8')
        f.write(ip_infors)
        f.write('\n')
        f.close()


if __name__ == '__main__':
    for i in range(1, 10):
        url = 'https://www.xicidaili.com/nn/{}'.format(i)
        headers = {
            'Host': 'www.xicidaili.com',
            'Referer': 'https://www.xicidaili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        ip_infors = get_ipInfors(url, headers=headers)
        print(ip_infors)
        # proxies = write_ipInfors(ip_infors)
