'''
Author: galeliu
Date: 2024-09-27 12:15:34
LastEditTime: 2024-09-27 13:13:50
LastEditors: galeliu
Description: .
'''
import pandas as pd
import time
import numpy as np

# excel1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\银行数据0926.xlsx"
# df = pd.read_excel(excel1)
# print(df)
# cols = df.columns
# print(cols)
# # bank_name_list = list(set(df['bank_name'].tolist()))
# # print(bank_name_list)
# # 按区域分组
# df_grouped = df.groupby('adname')
# df_res = pd.DataFrame(columns=cols)
# # 遍历每个组
# for name, group in df_grouped:
#     tmp_bank_list = list(set(df['bank_name'].tolist()))
#     # 逐一加入每个银行
#     tmp_group_list = [(ind, row['bank_name']) for ind, row in group.iterrows()]
#     print(tmp_group_list)
#     while len(tmp_group_list) > 0:
#         ind, bank_name = tmp_group_list[0]
#         print(ind, bank_name)
#         bank_list1 = tmp_bank_list
#         bank_list2 = [bank_name for _, bank_name in tmp_group_list]
#         # 如果bank_list1,bank_list2有交集
#         if set(bank_list1) & set(bank_list2):
#             if bank_name in tmp_bank_list:
#                 tmp_bank_list.remove(bank_name)
#                 tmp_group_list.remove((ind, bank_name))
#                 df_res.loc[len(df_res)] = df.loc[ind]
#             else:
#                 tmp_group_list.remove((ind, bank_name))
#                 tmp_group_list.append((ind, bank_name))
#         else:
#             tmp_bank_list = list(set(df['bank_name'].tolist()))
#         # time.sleep(0.1)
#         # print(tmp_group_list)
#     # print(df_res)
#     # break
# print(df_res)
# df_res.to_excel(
#     r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\银行数据0926_clean.xlsx", index=False)


# excel1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\银行数据0926.xlsx"
# df = pd.read_excel(excel1)
# print(df)
# # 对原始数据进行排序
# df = df.sort_values(by=['adname', 'bank_name'])

# # 按区域分组
# grouped = df.groupby('adname')

# # 创建一个新的DataFrame，用于存储打散后的数据
# shuffled_df = pd.DataFrame(columns=df.columns)

# # 对于每个区域，将其支行随机分配到新的DataFrame中
# for adname, group in grouped:
#     num_rows = len(shuffled_df[shuffled_df['adname'] == adname])
#     new_rows = []
#     for i in range(len(group)):
#         # 检查列表是否为空
#         available_positions = [j for j in range(num_rows + i) if (j == 0 or (j-1 >= 0 and shuffled_df.loc[j-1, 'bank_name'] != group.iloc[i]['bank_name'])) and (
#             j == num_rows + i - 1 or (j+1 < len(shuffled_df) and shuffled_df.loc[j+1, 'bank_name'] != group.iloc[i]['bank_name']))]
#         if not available_positions:
#             # 如果列表为空，直接将当前支行添加到新的DataFrame中
#             new_row = group.iloc[i].copy()
#             new_row['adname'] = adname
#             new_rows.append(new_row)
#         else:
#             # 随机选择一个插入位置
#             insert_index = np.random.choice(available_positions)
#             new_row = group.iloc[i].copy()
#             new_row['adname'] = adname
#             new_rows.append(new_row)
#     # 使用pd.concat将新的行添加到shuffled_df中
#     shuffled_df = pd.concat(
#         [shuffled_df, pd.DataFrame(new_rows)], ignore_index=True)

# print(shuffled_df)
# shuffled_df.to_excel(
#     r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\银行数据0926_clean.xlsx", index=False)


excel1 = r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\银行数据0926.xlsx"
df = pd.read_excel(excel1)
print(df)
cols = df.columns
print(cols)
# bank_name_list = list(set(df['bank_name'].tolist()))
# print(bank_name_list)
# 按区域分组
df_grouped = df.groupby('adname')
df_res = pd.DataFrame(columns=cols)
# 遍历每个组
for name, group in df_grouped:
    # tmp_bank_list = list(set(df['bank_name'].tolist()))
    # group内随机排序
    while True:
        group = group.sample(frac=1).reset_index(drop=True)
        bank_list = group['bank_name'].tolist()
        bank_pre = ''
        flg = 1
        for bank in bank_list:
            if bank == bank_pre:
                flg = 0
                break
            bank_pre = bank
        if flg == 1:
            break
    print(group)
    # 遍历每个组内的行
    for index, row in group.iterrows():
        df_res.loc[len(df_res)] = group.loc[index]

print(df_res)
df_res.to_excel(
    r"D:\work\workcode\work-github\work-yayu\gaode_api_scrapy\data\银行数据0926_clean.xlsx", index=False)
