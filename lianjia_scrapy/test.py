'''
Author: galeliu
Date: 2024-09-19 13:07:54
LastEditTime: 2024-09-20 15:23:53
LastEditors: galeliu
Description: .
'''
import pandas as pd

# csv_file = r'./data/gaoxin_xiaoqu_link.csv'
# df = pd.read_csv(csv_file, sep='\t', encoding='utf-8-sig',
#                  header=None, names=['xiaoqu_name', 'xiaoqu_url'])
# # df.to_csv(r'./data/gaoxin_xiaoqu_link2.csv', encoding='utf-8-sig', index=False)
# df.to_excel(r'./data/gaoxin_xiaoqu_link.xlsx')


# 匹配小区建成年
xiaoqu_file = r'./data/gaoxin_xiaoqu_link.xlsx'
house_file = r'./data/gaoxin_house_info.xlsx'
df_xiaoqu = pd.read_excel(xiaoqu_file)
df_xiaoqu = df_xiaoqu[['xiaoqu_url', 'xiaoqu_jiancheng_year']]
df_house = pd.read_excel(house_file)
# 删除xiaoqu_jiancheng_year列
# df_house = df_house.drop(columns=['xiaoqu_jiancheng_year'])
df = pd.merge(df_xiaoqu, df_house, on='xiaoqu_url')
print(df)
df.to_excel(r'./data/gaoxin_house_info_year.xlsx', index=False)
