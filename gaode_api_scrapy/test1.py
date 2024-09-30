'''
Author: galeliu
Date: 2024-09-25 19:08:12
LastEditTime: 2024-09-26 12:57:41
LastEditors: galeliu
Description: .
'''
import pandas as pd
# # 筛选出外呼沟通过数据中，电话为座机的数据
# excel1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank线上外呼沟通.xlsx"
# df1 = pd.read_excel(excel1)
# print(df1)
# # 剔除电话为空的数据
# df1 = df1[df1['电话'].notna()]
# print(df1)
# # 电话不是1开头的数据
# cols = ['bank_name', 'id', 'name', 'tel', '座机']
# df2 = pd.DataFrame(columns=cols)
# # df1 = df1[df1['电话'].str.startswith('1') == False]
# for ind, row in df1.iterrows():
#     if str(row['电话']).startswith('1') == False:
#         print(row['电话'])
#         df2.loc[ind] = [row['bank_name'], row['id'],
#                         row['name'], row['tel'], row['电话']]
# print(df2)
# # 合并座机和电话
# df2['zuoji'] = df2['tel'].astype(str)+';'+df2['座机'].astype(str)
# df2.to_excel(
#     r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank线上外呼沟通_座机.xlsx", index=False)


# excel1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank线上外呼沟通_座机.xlsx"
# df1 = pd.read_excel(excel1)
# df1 = df1[['id', 'zuoji']]
# print(df1)
# excel2 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all.xlsx"
# df2 = pd.read_excel(excel2)
# print(df2)
# # 合并两个表格
# df3 = pd.merge(df1, df2, on='id', how='right')
# print(df3)
# df3['座机'] = df3.apply(lambda row: row['tel'] if pd.isna(row['zuoji'])
#                       else row['zuoji'], axis=1)
# df3.to_excel(
#     r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all1.xlsx", index=False)


excel1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all.xlsx"
# excel1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all_gaode_and_tianyan.xlsx"
df1 = pd.read_excel(excel1)
print(df1)
excel2 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\【天眼查】企业搜索“银行”20240924(W20092410781727154839048).xlsx"
df2 = pd.read_excel(excel2)
print(df2)
df3 = pd.DataFrame()
n = 0
for ind, row in df1.iterrows():
    print('{}/{}'.format(n, len(df1)))
    n += 1
    # # 仅处理tianyan_zuoji为空的数据
    # if not pd.isna(row['tianyan_zuoji']):
    #     continue
    bank_name = row['name']
    bank_pre = row['bank_name']
    if bank_pre == '成都农商银行':
        bank_pre = '农村商业银行'
    elif bank_pre == '邮储银行':
        bank_pre = '邮政储蓄银行'
    elif bank_pre == '浦发':
        bank_pre = '浦东发展银行'
    elif bank_pre == '绵阳商业银行':
        bank_pre = '绵阳市商业银行'
    bank_sub = ''
    # 提取括号内内容:成都农商银行(青羊支行)
    if '(' in bank_name:
        bank_sub = bank_name[bank_name.find('(')+1:bank_name.find(')')]
    print(bank_pre)
    print(bank_sub)
    bank_tag = ''
    if '支行' in bank_sub:
        bank_tag = bank_sub[:bank_sub.find('支行')]
    elif '分理' in bank_sub:
        bank_tag = bank_sub[:bank_sub.find('分理')]
    print(bank_tag)
    if bank_tag:
        # 通过bank_pre和bank_tag在df2中查找
        for jnd, jow in df2.iterrows():
            tianyan_name = jow['公司名称']
            tianyan_zuoji = str(jow['联系电话']) + ';' + str(jow['其他电话'])
            if bank_pre in tianyan_name and bank_tag in tianyan_name:
                print(tianyan_name)
                df1.loc[ind, ['tianyan_name', 'tianyan_zuoji']] = [
                    tianyan_name, tianyan_zuoji]
                break
    # print(df1.loc[ind])
    # break
print(df1)
df1.to_excel(
    r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\bank_all_gaode_and_tianyan.xlsx", index=False)
