import pandas as pd


csv_file = r'comment_info_背债1_gpt_result.csv'
df = pd.read_csv(csv_file, sep='\t')
print(df)
# df_group = df.groupby('is_want_debt').size().sort_values(ascending=False)
# # df_group.sort_values(by='count', replace=True)
# print(df_group)
df = df[df['is_want_debt'].isin(['是', '否'])]
print(df)
df['is_want_debt'] = df['is_want_debt'].map(lambda x:'yes' if x == '是' else 'no')
df.to_csv('comment_info_背债1_gpt_result_processed.csv', sep='\t', index=False)