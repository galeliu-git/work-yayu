'''
Author: galeliu
Date: 2024-09-09 16:30:13
LastEditTime: 2024-09-20 14:45:56
LastEditors: galeliu
Description: .
'''
# url = "https://www.zhipin.com/"

from DrissionPage import ChromiumPage, WebPage, SessionPage, ChromiumOptions
import time
import csv
import random
import pandas as pd
import os
import schedule
import json
import get_kuaidaili_ip


page = ChromiumPage(9333)
# print(page)
# print(page.ele('.title'))


# 爬取小区链接
def search_xiaoqu():
    url = "https://cd.ke.com/xiaoqu/gaoxin7/"
    data_save_path = 'data/gaoxin_xiaoqu_link.csv'
    writer_data_info = csv.writer(
        open(data_save_path, 'a', newline='',  encoding='utf-8-sig'), delimiter='\t')
    # page = ChromiumPage()
    page.get(url)

    # page.ele('.ipt-search').input(keyword)
    # page.ele('.btn btn-search').click()
    n = 1
    while True:
        print(f'正在爬取第{n}页')
        n += 1
        xiaoqu_li_list = page.ele('.listContent').eles('@tag()=li')
        for xiaoqu_li in xiaoqu_li_list:
            # print('xiaoqu_li', xiaoqu_li)
            xiaoqu_name = xiaoqu_li.ele('.maidian-detail').text
            xiaoqu_url = xiaoqu_li.ele('.maidian-detail').link
            print(xiaoqu_name, xiaoqu_url)
            writer_data_info.writerow([xiaoqu_name, xiaoqu_url])
            # break
        # 如果不存在【下一页】按钮，则退出循环
        if not page.ele('.page-box house-lst-page-box').ele('@text()=下一页'):
            print('没有下一页了')
            break
        # 点击下一页
        page.ele('.page-box house-lst-page-box').ele('@text()=下一页').click()
        time.sleep(random.uniform(1, 5))
        # break
    # # 关闭page
    # page.quit()
    # writer_data_info.close()
    print('爬取完成')


# 爬取小区房源信息
def search_house_from_xiaoqu(xiaoqu_url):
    # co = ChromiumOptions().auto_port()
    # ip_proxy = get_kuaidaili_ip.get_available_proxy()
    # print(ip_proxy)
    # co.set_proxy(ip_proxy)  # 代理IP:端口号
    # page = ChromiumPage(co)
    page.get(xiaoqu_url)
    time.sleep(random.uniform(2, 5))
    xiaoqu_name = page.ele('.title-wrapper').ele('.main').text
    print(xiaoqu_name)
    print(xiaoqu_url)
    xiaoqu_jiancheng_year = ''
    if page.ele('@text()=建成年代'):
        xiaoqu_jiancheng_year = page.ele(
            '@text()=建成年代').parent().ele('.xiaoquInfoContent').text
        # print(xiaoqu_jiancheng_year)
    # 小区历史成交
    deal_info_list = []
    lowest_price = 999999
    if page.ele('.frameDealListItem'):
        deal_info_eles = page.ele('.frameDealListItem').eles('@tag()=li')
        for deal_info_ele in deal_info_eles:
            deal_info_dict = {}
            deal_info_dict['huxing'] = deal_info_ele.ele(
                '.frameDealTitle').text
            deal_info_dict['house_url'] = deal_info_ele.ele(
                '.frameDealTitle').link
            deal_info_dict['floor'] = deal_info_ele.ele('.frameDealFloor').text
            deal_info_dict['house_jiancheng_year'] = deal_info_ele.ele(
                '.frameDealResblock').text
            deal_info_dict['area'] = deal_info_ele.ele('.frameDealArea').text
            deal_info_dict['deal_date'] = deal_info_ele.ele(
                '.frameDealDate').text
            deal_info_dict['deal_price'] = deal_info_ele.ele(
                '.frameDealPrice').text
            deal_info_dict['unit_price'] = deal_info_ele.ele(
                '.frameDealUnitPrice').text
            deal_info_list.append(deal_info_dict)
        # print(deal_info_list)
        for i in [i['unit_price'] for i in deal_info_list]:
            if '元/平' in i:
                i = i.replace('元/平', '')
                if int(i) < lowest_price:
                    lowest_price = int(i)
    # print(lowest_price)
    # 查看小区全部二手房源
    if page.ele('@text()=查看小区全部在售二手房'):
        page.ele('@text()=查看小区全部在售二手房').click()
        # time.sleep(random.uniform(1, 5))
    else:
        print('没有在售二手房')
        # # 关闭页面
        # page.quit()
        return []
    time.sleep(random.uniform(2, 5))
    # 爬取房源信息
    print('开始爬取房源信息')
    res_data_list = []
    n = 1
    while True:
        print(f'正在爬取第{n}页')
        n += 1
        house_info_eles = page.ele('.sellListContent').eles('.info clear')
        # house_info_eles = page.ele('.sellListContent').eles('@tag()=li')
        # print('house_info_eles', house_info_eles)
        for house_info_ele in house_info_eles:
            data_dict = {}
            house_title = house_info_ele.ele('.title').text
            house_url = house_info_ele.ele('.title').ele('@tag()=a').link
            house_base_info = house_info_ele.ele('.houseInfo').text
            house_total_price = house_info_ele.ele(
                '.totalPrice totalPrice2').text
            house_unit_price = house_info_ele.ele('.unitPrice').text
            # print(house_title, house_url, house_base_info,
            #       house_total_price, house_unit_price)
            data_dict['xiaoqu_name'] = xiaoqu_name
            data_dict['xiaoqu_url'] = xiaoqu_url
            data_dict['deal_info_list'] = str(deal_info_list)
            data_dict['lowest_price'] = lowest_price
            data_dict['house_title'] = house_title
            data_dict['house_url'] = house_url
            data_dict['house_base_info'] = house_base_info
            data_dict['house_total_price'] = house_total_price
            data_dict['house_unit_price'] = int(house_unit_price[:house_unit_price.find(
                '元/平')].replace(',', '')) if '元/平' in house_unit_price else ''
            res_data_list.append(data_dict)
        # 翻页
        page_num_box_ele = page.ele('.page-box house-lst-page-box')
        # print('page_num_box_ele', page_num_box_ele)
        # print(page_num_box_ele.attrs)
        page_data_dict = json.loads(page_num_box_ele.attrs['page-data'])
        # print('page_data_dict', page_data_dict)
        total_page = page_data_dict['totalPage']
        cur_page = page_data_dict['curPage']
        if cur_page >= total_page:
            print('没有下一页了')
            break
        else:
            page.ele(
                '.page-box house-lst-page-box').ele('@text()={}'.format(cur_page + 1)).click()
        time.sleep(random.uniform(1, 5))
        # break
    # # 关闭页面
    # page.quit()
    return res_data_list


# 批量爬取房源
def batch_crawl_house():
    xiaoqu_link_file = r'data/gaoxin_xiaoqu_link.xlsx'
    house_info_path = r'data/gaoxin_house_info.xlsx'
    # df_xiaoqu_link = pd.read_csv(
    #     xiaoqu_link_file, sep='\t', encoding='utf-8-sig', header=None, names=['xiaoqu_name', 'xiaoqu_url'])
    df_xiaoqu_link = pd.read_excel(xiaoqu_link_file)
    df_xiaoqu_link_need_crawl = df_xiaoqu_link[df_xiaoqu_link['if_crawled'] != 1]
    print(df_xiaoqu_link_need_crawl)
    if os.path.exists(house_info_path):
        df_house_data = pd.read_excel(house_info_path)
    else:
        columns = ['xiaoqu_name', 'xiaoqu_url',
                   'deal_info_list', 'lowest_price', 'house_title', 'house_url', 'house_base_info', 'house_total_price', 'house_unit_price']
        df_house_data = pd.DataFrame(columns=columns)
    xiaoqu_crawled_list = list(set(df_house_data['xiaoqu_name'].tolist()))
    n = 1
    for index, row in df_xiaoqu_link_need_crawl.iterrows():
        print('正在爬取第{}/{}个小区'.format(n, len(df_xiaoqu_link_need_crawl)))
        n += 1
        xiaoqu_name = row['xiaoqu_name']
        xiaoqu_url = row['xiaoqu_url']
        if xiaoqu_name in xiaoqu_crawled_list:
            print('已经爬取过该小区了')
            continue
        # print('正在爬取小区：', xiaoqu_name)
        try:
            res_data_list = search_house_from_xiaoqu(xiaoqu_url)
            for data_dict in res_data_list:
                add_ind = len(df_house_data)
                df_house_data.loc[add_ind] = data_dict
            df_house_data.to_excel(house_info_path, index=False)
            # 爬过的小区标记
            df_xiaoqu_link.loc[index, 'if_crawled'] = 1
            df_xiaoqu_link.to_excel(xiaoqu_link_file, index=False)
        except Exception as e:
            print('爬取失败', e)
            continue
        time.sleep(random.uniform(1, 5))
        # print(df_house_data)
        # break
    return


if __name__ == '__main__':
    # search_xiaoqu()
    xiaoqu_url = 'https://cd.ke.com/xiaoqu/1611041846447/'
    # res_data_list = search_house_from_xiaoqu(xiaoqu_url)
    # print(res_data_list)
    # print(1)
    batch_crawl_house()
