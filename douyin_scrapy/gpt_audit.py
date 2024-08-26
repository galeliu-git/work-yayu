'''
Author: galeliu
Date: 2024-07-31 10:25:20
LastEditTime: 2024-07-31 16:40:12
LastEditors: galeliu
Description: .
'''
import pandas as pd
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import time
import csv


start_time = time.time()
api_key = '286bd4c2e06eac46c294180fbeca3948.J0y2r3whdNUzfC4a'
llm = ChatOpenAI(
    temperature=0.95,
    model="glm-4-flash",
    openai_api_key=api_key,
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            '''你是一个审核机器人，你判断的内容是一些关于【背债】的视频下的用户评论，你的目的是识别出哪些用户在评论里表达了愿意、想背债的诉求，不要评论里表达出支持、肯定的内容，只要能从评论里看出评论人想要自己去背债的内容
我发给你的所有内容就是评论信息，你只需回复【是】或【否】即可，不要有任何多余回答
内容中明确表达了“我想”、“我要”等意愿或者询问“靠谱的”“怎么做”“如何做”“如何操作”等才回复【是】，比如：
question:我也想背
answer:是
question:我什么都没有我贷款没钱还咋办[捂脸][捂脸][捂脸]
answer:否
question:有没有靠谱的中介，给贷些
answer:是
question:有靠谱的操作公司吗
answer:是'''
        ),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

# memory = ConversationBufferMemory(
#     memory_key="chat_history", return_messages=True)
# print(memory)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    # verbose=True,
)
# prompt = '''本人从不网货，不熟悉电话不接，不乱按链接，做人脚踏实地怎么可能被骗。'''
# print(conversation.invoke({"question": prompt}))
comment_file = r'comment_info_背债1.csv'
df = pd.read_csv(comment_file, sep='\t')
# df = df.sample(10)

res_file = '_gpt_result'.join(os.path.splitext(comment_file))
# 已审核评论
df_audited = pd.read_csv(res_file,sep='\t')
audited_videl_url_list = list(set(df_audited['video_url'].to_list()))

# 审核结果写入文件
writer_comment_info = csv.writer(
    open(res_file, 'a', newline='', encoding='utf-8'), delimiter='\t')
comment_info_columns = ['video_url', 'title', 'comment_user',
                        'comment_text', 'comment_time', 'comment_location', 'comment_user_url', 'is_want_debt']
# writer_comment_info.writerow(comment_info_columns)
for index, row in df.iterrows():
    try:
        content = str(row['comment_text']).strip()
        # 如果内容为空或者为nan，则跳过
        if (not content) or (content =='nan'):
            continue
        # 如果已经审核过，则跳过
        if row['video_url'] in audited_videl_url_list:
            continue
        content = content.replace('\n', '。').strip()
        res = conversation.invoke({"question": content})
        print(index)
        print(res)
        out_put = res['text']
        res_list = [
            row['video_url'],
            row['title'],
            row['comment_user'],
            row['comment_text'],
            row['comment_time'],
            row['comment_location'],
            row['comment_user_url'],
            out_put,

        ]
        writer_comment_info.writerow(res_list)
    except Exception as e:
        error_info = '{}\t{}\t{}\n'.format(row['video_url'], row['comment_text'], e)
        print(error_info)
        with open('error_audit.txt', 'a', encoding='utf-8') as f:
            f.write(error_info)
    # df.loc[index, 'is_want_debt'] = out_put
# df.to_csv('sample_comment_info_背债_audit_result.csv', sep='\t', index=False)
# 统计执行耗时
print(f"执行耗时: {time.time() - start_time}秒")
