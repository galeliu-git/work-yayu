'''
Author: galeliu
Date: 2024-09-09 12:36:39
LastEditTime: 2024-09-18 13:12:40
LastEditors: galeliu
Description: .
'''
import os
from playwright.sync_api import sync_playwright
import pandas as pd


data_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
save_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款1.csv'
df = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
print(df)
df.loc[df['if_contact'].isnull(), 'if_contact'] = 0
df.loc[df['if_continue_contact'].isnull(), 'if_continue_contact'] = 0


print(df)
df.to_csv(save_file, sep='\t', encoding='utf-8-sig', index=False)


# excel_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\银行.xlsx'
# df = pd.read_excel(excel_file, sheet_name=None)
# print(df.keys())
# df_list = []
# for sheet_name in df.keys():
#     tmp_df = df[sheet_name]
#     print(tmp_df)
#     tmp_df['银行名'] = sheet_name
#     df_list.append(tmp_df)
# df_final = pd.concat(df_list)
# print(df_final)
# df_final.to_excel(
#     r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\银行_汇总.xlsx', index=False)

# data_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
# df1 = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
# print(df1)
# data_file2 = r"D:\work\workcode\work-github\work-yayu\boss_scrapy\data\职位-已爬取-贷款.xlsx"
# df2 = pd.read_excel(data_file2)
# print(df2)
# df2_filter = df2[df2['if_keep'] != 0]
# print(df2_filter)
# jobs_url_list = df2_filter['job_url'].tolist()
# # 保留df1中job_url在jobs_url_list中的行
# df1_final = df1[df1['job_url'].isin(jobs_url_list)]
# print(df1_final)
# df1_final.to_csv(data_file, sep='\t', encoding='utf-8-sig', index=False)
