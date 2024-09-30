'''
Author: galeliu
Date: 2024-09-20 12:04:58
LastEditTime: 2024-09-20 17:32:19
LastEditors: galeliu
Description: .
'''
# 1. 删除重复行
# 2. 房源总价格200-350w
# 3. 小区建成时间在2010年以后
# 4. 剔除小区无历史最低价的数据
# 5. 房源单价低于小区历史最低成交价
# 6. 同小区取最低的10套


import pandas as pd
import os


source_file = r"D:\work\workcode\work-github\work-yayu\lianjia_scrapy\data\gaoxin_house_info_year.xlsx"
target_file = r"D:\work\workcode\work-github\work-yayu\lianjia_scrapy\data\gaoxin_house_info_clean.xlsx"
df = pd.read_excel(source_file)
print('原始数据：', df)
# 删除重复行
df.drop_duplicates(subset=['house_url'], inplace=True)
print('删除重复行后：', df)
# 筛房源价格
# 删除house_total_price没有数字的行
df = df[df['house_total_price'].str.contains('\d')]
df['house_total_price_num'] = df['house_total_price'].str.replace(
    '万', '').astype(float)
df = df[(df['house_total_price_num'] >= 200) &
        (df['house_total_price_num'] <= 350)]
print('筛选房源价格后：', df)
# 筛小区建成时间
df['xiaoqu_jiancheng_year_num'] = df['xiaoqu_jiancheng_year'].map(
    lambda x: int(x.split('-')[1]) if '-' in str(x) else x)
df = df[df['xiaoqu_jiancheng_year_num'].notnull()]
df = df[df['xiaoqu_jiancheng_year_num'].astype(int) >= 2010]
print('筛选小区建成时间后：', df)
# 剔除小区无历史最低价的数据
df = df[df['lowest_price'] < 999999]
print('剔除小区无历史最低价的数据后：', df)
# 筛单价
df['target_price'] = df['lowest_price'] * 1
df = df[df['house_unit_price'] <= df['target_price']]
print('筛选单价后：', df)
# 同小区取最低的10套
df = df.sort_values(by=['house_unit_price'])
df = df.groupby('xiaoqu_name').head(10)
print('同小区取最低的10套后：', df)
df.to_excel(target_file, index=False)
