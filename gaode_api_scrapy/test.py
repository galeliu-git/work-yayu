'''
Author: galeliu
Date: 2024-09-14 15:30:35
LastEditTime: 2024-09-26 19:09:52
LastEditors: galeliu
Description: .
'''
import pandas as pd
# excel_file1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_pos_gaode.xlsx"
# df1 = pd.read_excel(excel_file1)
# print(df1)
# # 去重
# df1.drop_duplicates(subset=['id'], inplace=True)
# # tel不为空的行
# df1 = df1[df1['tel'].notna()]
# # 筛选tel字符数大于5的
# df1 = df1[df1['tel'].str.len() > 5]
# print(df1)
# df1.to_excel(
#     r'D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all.xlsx', index=False)


# yidayin_file = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\已打印.xlsx"
# df2 = pd.read_excel(yidayin_file)
# print(df2)
# # 筛选未打印的数据
# df3 = df1[~df1['id'].isin(df2['id'])]
# print(df3)
# df_final = df3[['bank_name', 'id', 'name', 'tel']]
# df_final['客户经理'] = ''
# df_final['电话'] = ''
# df_final['备注'] = ''
# df_final.to_excel(
#     r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\未打印.xlsx", index=False)

excel1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\汇总3.xlsx"
df1 = pd.read_excel(excel1)
df1 = df1[['银行.1', '客户经理', '联系方式']]
# 联系方式去重
df1.drop_duplicates(subset=['联系方式'], inplace=True)
print(df1)
excel2 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all.xlsx"

df2 = pd.read_excel(excel2)
# 银行名去重
df2.drop_duplicates(subset=['name'], inplace=True)
print(df2)
# df2.to_excel(
#     r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all.xlsx", index=False)
df3 = pd.merge(df1, df2, left_on='银行.1', right_on='name', how='left')
print(df3)
# df3.to_excel(
#     r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all_已沟通.xlsx", index=False)
df3.to_excel(
r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all_未匹配.xlsx", index=False)
