import pandas as pd


csv_file = r'data/comment_info_撸贷.csv'
df = pd.read_csv(csv_file, sep='\t')
print(df)
print('去重前量级：', len(df))
# 按cid去重
df = df.drop_duplicates(subset=['cid'])
print('去重后量级：', len(df))
