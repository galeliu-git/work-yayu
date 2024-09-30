'''
Author: galeliu
Date: 2024-09-13 16:50:17
LastEditTime: 2024-09-18 19:00:45
LastEditors: galeliu
Description: .
'''
import pandas as pd
import os


data_file = r"D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv"
yidayin_file = r"D:\work\workcode\work-github\work-yayu\boss_scrapy\data\贷款电话_已打印.xlsx"
save_file = r"D:\work\workcode\work-github\work-yayu\boss_scrapy\data\贷款电话_all.xlsx"
not_printed_file = r"D:\work\workcode\work-github\work-yayu\boss_scrapy\data\贷款电话_未打印.xlsx"
df = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
print(df)
df_final = df[~df['number'].isnull()]
print(df_final)
df_final.reset_index(drop=True, inplace=True)
df_final.to_excel(save_file)
df_printed = pd.read_excel(yidayin_file)
df_not_printed = df_final[~df_final['number'].isin(df_printed['number'])]
df_not_printed = df_not_printed[['jobName', 'brandName', 'number']]
df_not_printed.reset_index(drop=True, inplace=True)
df_not_printed.to_excel(not_printed_file)
# df['phone_num'] = df['phone_num'].apply(lambda x: re.findall(r'\d{11}', x))
# df.to_csv(r'"D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv"', index=False)
