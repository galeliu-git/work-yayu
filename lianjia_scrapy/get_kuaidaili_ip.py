'''
Author: galeliu
Date: 2024-09-19 14:16:37
LastEditTime: 2024-09-20 11:31:57
LastEditors: galeliu
Description: .
'''

#!/usr/bin/env Python
# -*- coding: utf-8 -*-

"""
使用requests请求代理服务器
请求http和https网页均适用
"""


# 提取代理API接口，获取1个代理IP


# 获取新的代理IP




import requests
def get_new_proxies():
    secret_id = "z8mv1jeqe7icysl4icgmobxjbks65ns3"
    signature = secret_id
    api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=o2dm14lvtrrwhwxvxkko&signature={}&num=1&pt=1&sep=1".format(
        signature)

    # 获取API接口返回的代理IP
    proxy_ip = requests.get(api_url).text

    # 用户名密码认证(私密代理/独享代理)
    username = "d2568368155"
    password = "vv5yyjgx"
    proxies = {
        "http": "http://%(proxy)s" % {"proxy": proxy_ip},
        "https": "http://%(proxy)s" % {"proxy": proxy_ip}
    }
    # proxies = {
    #     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    #     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
    # }
    return proxies


# 获取可用ip
def get_available_proxy():
    # 从ip池中获取代理ip
    ip_pool_txt = open('ip_pool.txt', 'r')
    ip_pool = ip_pool_txt.readlines()
    ip_pool_txt.close()
    if len(ip_pool) == 0:
        # 获取新的代理IP
        proxies = get_new_proxies()
        # 将新的代理IP写入ip_pool.txt
        ip_pool_txt = open('ip_pool.txt', 'w')
        ip_pool_txt.write(proxies['https']+'\n')
        ip_pool_txt.close()
        return proxies['https']
    else:
        # 验证ip是否可用
        for ip_proxy in ip_pool:
            proxy_ip = ip_proxy.strip()
            try:
                # 要访问的目标网页
                target_url = "https://dev.kdlapi.com/testproxy"
                # 使用代理IP发送请求
                response = requests.get(target_url, proxies={
                                        "https": proxy_ip}, timeout=3)
                # 获取页面内容
                if response.status_code == 200:
                    return proxy_ip
            except:
                pass
        # 如果所有ip都不可用，则获取新的代理IP
        proxies = get_new_proxies()
        # 将新的代理IP写入ip_pool.txt
        ip_pool_txt = open('ip_pool.txt', 'w')
        ip_pool_txt.write(proxies['https']+'\n')
        ip_pool_txt.close()
        return proxies['https']

    # 白名单方式（需提前设置白名单）
    # proxies = {
    #     "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
    #     "https": "http://%(proxy)s/" % {"proxy": proxy_ip}
    # }

    # # 要访问的目标网页
    # target_url = "https://dev.kdlapi.com/testproxy"

    # # 使用代理IP发送请求
    # response = requests.get(target_url, proxies=proxies)

    # # 获取页面内容
    # if response.status_code == 200:
    #     print(response.text)


if __name__ == '__main__':

    # print(proxies)
    from DrissionPage import WebPage, ChromiumOptions, ChromiumPage
    import time
    # proxies = get_proxies()
    co = ChromiumOptions().auto_port()
    ip_proxy = get_available_proxy()
    print(ip_proxy)
    co.set_proxy(ip_proxy)  # 代理IP:端口号
    page = ChromiumPage(co)
    # page = WebPage(chromium_options=co)
    # 要访问的目标网页
    # page.get("https://httpbin.org/get")
    # page.get("https://dev.kdlapi.com/testproxy")
    page.get("https://cd.ke.com/xiaoqu/3011053387628/")

    # 获取页面内容
    print(page.html)
    # print(proxies)
