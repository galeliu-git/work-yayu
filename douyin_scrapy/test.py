'''
Author: galeliu
Date: 2024-07-30 09:58:39
LastEditTime: 2024-08-01 09:39:13
LastEditors: galeliu
Description: .
'''
import pandas as pd


# df1 = pd.read_csv('video_info_背债.csv', sep='\t')
# df2 = pd.read_csv('comment_info_背债.csv', sep='\t')
# df1 = df1[['url', 'title']]
# df1['video_url'] = df1['url']
# print(df1)
# print(df2)
# df3 = pd.merge(df2, df1, how='left', left_on='video_url', right_on='video_url')
# print(df3)

# df3.to_csv('comment_info_背债1.csv', sep='\t', index=False)

# df = pd.read_csv('comment_info_背债1.csv', sep='\t')
# df_sample = df.sample(n=1000)
# df_sample.to_csv('sample_comment_info_背债.csv', sep='\t', index=False)
# df = pd.read_csv('video_url_背债.txt', sep='\t')
# with open(r'video_url_背债.txt', 'r') as f:
#     lines = f.readlines()
#     lines = [line.strip() for line in lines]
#     print(len(lines))
#     print(len(list(set(lines))))
