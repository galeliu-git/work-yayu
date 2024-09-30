'''
Author: galeliu
Date: 2024-09-19 14:43:56
LastEditTime: 2024-09-20 15:02:38
LastEditors: galeliu
Description: .
'''
from DrissionPage import ChromiumPage, WebPage, SessionPage, ChromiumOptions
import time
import csv
import random
import pandas as pd
import os
import schedule
import json
import get_kuaidaili_ip

page = ChromiumPage(9335)
# 爬取小区房源信息


def search_xiaoqu_year(xiaoqu_url):
    # co = ChromiumOptions().auto_port()
    # ip_proxy = get_kuaidaili_ip.get_available_proxy()
    # print(ip_proxy)
    # co.set_proxy(ip_proxy)  # 代理IP:端口号
    # page = ChromiumPage(co)
    page.get(xiaoqu_url)
    time.sleep(random.uniform(2, 5))
    print(xiaoqu_url)
    xiaoqu_jiancheng_year = ''
    if page.ele('@text()=建成年代'):
        xiaoqu_jiancheng_year = page.ele(
            '@text()=建成年代').parent().ele('.xiaoquInfoContent').text
        xiaoqu_jiancheng_year = xiaoqu_jiancheng_year.replace('年', '')
    return xiaoqu_jiancheng_year


xiaoqu_link_file = r'data/gaoxin_xiaoqu_link.xlsx'
df_xiaoqu_link = pd.read_excel(xiaoqu_link_file)
# 筛选出不为空的数据
df_xiaoqu_link_need_crwal = df_xiaoqu_link[df_xiaoqu_link['xiaoqu_jiancheng_year'].isnull(
)]
n = 1
for ind, row in df_xiaoqu_link_need_crwal.iterrows():
    print('第{}/{}个'.format(n, len(df_xiaoqu_link_need_crwal)))
    n += 1
    xiaoqu_jiancheng_year = search_xiaoqu_year(row['xiaoqu_url'])
    df_xiaoqu_link.loc[ind, 'xiaoqu_jiancheng_year'] = xiaoqu_jiancheng_year
    df_xiaoqu_link.to_excel(xiaoqu_link_file, index=False)
