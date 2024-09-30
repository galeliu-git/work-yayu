'''
Author: galeliu
Date: 2024-09-13 19:07:41
LastEditTime: 2024-09-14 17:00:58
LastEditors: galeliu
Description: .
'''
import requests
import pandas as pd

api_key = '389dfed0fff068e13af33e78438cfbb4'


# 根据关键词搜索位置
def pos_search_by_keyword(keyword):
    base_url = 'https://restapi.amap.com/v5/place/text?key={}&keywords={}&region={}&page_size={}&page_num={}&citylimit=true&show_fields=business'
    region = '成都市'
    # keyword = '交通银行'
    page_size = 25
    page_num = 1
    pos_list = []
    while True:
        # while page_num <= 2:
        url = base_url.format(api_key, keyword, region, page_size, page_num)
        # print(url)
        response = requests.get(url)
        if response.json()['status'] == '1':
            # if response.json()['count'] == '0':
            #     break
            # print(response.json())
            data = response.json()['pois']
            pos_list += data
            if len(data) < page_size:
                break
            # print(data)
        else:
            print('请求失败')
            break
        page_num += 1
    # 去重
    # pos_list = list(set(pos_list))
    print('【{}】总量级：'.format(keyword), len(pos_list))
    return pos_list


def batch_search_pos():
    keyword_txt = r'data/bank.txt'
    data_file = r'data/bank_pos_gaode.xlsx'
    df = pd.read_excel(data_file)
    keywords_crawled = df['bank_name'].tolist()
    with open(keyword_txt, 'r', encoding='utf-8') as f:
        keywords = f.readlines()
        n = 1
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword in keywords_crawled:
                print('【{}】已爬取'.format(keyword))
                n += 1
                continue
            print('{}/{}'.format(n, len(keywords)))
            print('【{}】开始搜索'.format(keyword))
            res_data = pos_search_by_keyword(keyword+'营业厅')
            for item in res_data:
                index = len(df)
                df.loc[index, 'bank_name'] = keyword
                df.loc[index, 'id'] = item['id']
                df.loc[index, 'name'] = item['name']
                if 'cityname' in item:
                    df.loc[index, 'cityname'] = item['cityname']
                if 'adname' in item:
                    df.loc[index, 'adname'] = item['adname']
                if 'type' in item:
                    df.loc[index, 'type'] = item['type']
                if 'address' in item:
                    df.loc[index, 'address'] = item['address']
                if 'business_area' in item['business']:
                    df.loc[index, 'business_area'] = item['business']['business_area']
                if 'keytag' in item['business']:
                    df.loc[index, 'keytag'] = item['business']['keytag']
                if 'rectag' in item['business']:
                    df.loc[index, 'rectag'] = item['business']['rectag']
                if 'opentime_week' in item['business']:
                    df.loc[index, 'opentime_week'] = item['business']['opentime_week']
                if 'tel' in item['business']:
                    df.loc[index, 'tel'] = item['business']['tel']
            df.to_excel(data_file, index=False)
            n += 1
            # break


if __name__ == '__main__':
    batch_search_pos()
    # pos_search_by_keyword('恒丰银行营业厅')
