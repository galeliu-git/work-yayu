'''
Author: galeliu
Date: 2024-09-09 16:30:13
LastEditTime: 2024-09-11 11:51:23
LastEditors: galeliu
Description: .
'''
from DrissionPage import ChromiumPage, WebPage, SessionPage, ChromiumOptions
import time
import csv
import random
import pandas as pd
import os
# url = "https://www.zhipin.com/"
base_url = "https://www.zhipin.com/web/geek/job?query={}"
jobs_url_format = 'https://www.zhipin.com/job_detail/{}.html?lid={}1&securityId={}'
consultation_content_list = [
    '你好,不好意思打扰了，我想咨询一下个人做贷款，请问您这边有你们公司贷款业务员的联系方式吗？',
    '打扰了，不好意思，我想做贷款咨询，请问您这边有你们公司贷款业务员的联系方式吗？',
    '抱歉，打扰一下，我想做贷款，能给我介绍一个你们做贷款的人的联系方式吗？',
]

# 公司去重


def company_filter(data_file):
    # 按boss名字和公司名字去重
    df = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
    print('去重前数据量：', len(df))
    df.drop_duplicates(subset=['bossName', 'brandName'],
                       keep='first', inplace=True)
    df.to_csv(data_file, sep='\t', index=False, encoding='utf-8-sig')
    print('去重完成，去重后数据量：', len(df))
    return df


# 爬取职位链接
def search_jobs_links_by_keyword(keyword):
    data_save_path = 'data/jobs_links_{}.csv'.format(keyword)
    if os.path.exists(data_save_path):
        # df_comment_info = pd.read_csv(
        #     data_save_path, sep='\t', encoding='utf-8-sig')
        # video_list_crawled = list(set(df_comment_info['video_url'].tolist()))
        writer_data_info = csv.writer(
            open(data_save_path, 'a', newline='', encoding='utf-8-sig'), delimiter='\t')
    else:
        columns_list = ['jobName',  'bossName',
                        'cityName', 'brandName', 'job_url',]
        writer_data_info = csv.writer(
            open(data_save_path, 'a', newline='',  encoding='utf-8-sig'), delimiter='\t')
        writer_data_info.writerow(columns_list)
    page = ChromiumPage()
    # 监听数据包
    data_path_jobs_info = 'wapi/zpgeek/search/joblist'
    page.listen.start(targets=data_path_jobs_info)
    url = base_url.format(keyword)
    page.get(url)

    # page.ele('.ipt-search').input(keyword)
    # page.ele('.btn btn-search').click()
    n = 1
    while True:
        print(f'正在爬取第{n}页')
        n += 1
        # 等待数据包加载
        resp = page.listen.wait(timeout=10)
        jobs_info_json_data = resp.response.body
        jobs_list_data = jobs_info_json_data['zpData']['jobList']
        # print(jobs_list_data)
        # 解析遍历数据
        for job in jobs_list_data:
            jobName = job['jobName']
            encryptJobId = job['encryptJobId']
            lid = job['lid']
            securityId = job['securityId']
            job_url = jobs_url_format.format(encryptJobId, lid, securityId)
            bossName = job['bossName']
            cityName = job['cityName']
            brandName = job['brandName']
            # print(job_url)
            # 写入数据
            writer_data_info.writerow(
                [jobName, bossName, cityName, brandName, job_url])
        # 如果下一页的父级元素是disabled，则退出循环
        if page.ele('.ui-icon-arrow-right').parent(1).attrs['class'] == 'disabled':
            print('没有下一页了')
            break
        # 点击下一页
        page.ele('.ui-icon-arrow-right').click()
        time.sleep(random.uniform(1, 5))
        # break
    # # 关闭page
    # page.quit()
    print('爬取完成')
    company_filter(data_save_path)


# 与hr打招呼
def send_message_to_hr(job_url):
    # 输入内容
    consultation_content = random.choice(consultation_content_list)
    page = ChromiumPage()
    page.get(job_url)
    # 点击立即沟通
    if page.ele('.btn btn-startchat') and page.ele('.btn btn-startchat').text == '立即沟通':
        page.ele('.btn btn-startchat').click()
        time.sleep(random.uniform(1, 2))
        if page.ele('.btn btn-outline btn-cancel'):
            # 点击【留在此页】
            page.ele('.btn btn-outline btn-cancel').click()
        # 点击继续沟通
        if page.ele('.btn btn-startchat').text == '继续沟通':
            page.ele('.btn btn-startchat').click()
            # 等待页面加载
            time.sleep(random.uniform(1, 10))
            # 输入内容
            page.ele('.chat-input').input(consultation_content)
            # 点击发送
            # page.ele('@text()=发送').click()
            page.ele('.btn-v2 btn-sure-v2 btn-send').click()
        # page.ele('.input-area').input(consultation_content)

        print('打招呼成功')
    else:
        print('已经沟通过')
    return


# 爬取对话内容
def crawl_dialogue_content(url):
    page = ChromiumPage()
    page.get(url)
    # 点击【继续沟通】
    if page.ele('.btn btn-startchat').text == '继续沟通':
        page.ele('.btn btn-startchat').click()
        # 等待页面加载
        time.sleep(random.uniform(1, 10))
        # 获取对话内容
        dialogue_content = page.ele('.im-list').text
        print(dialogue_content)
    else:
        print('未沟通过')


# 批量自动化-打招呼
def batch_send_message():
    data_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
    df = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
    print(df)
    # df['if_contact'] = ''
    df_wait_contact = df[df['if_contact'].isnull()]
    print(df_wait_contact)
    n = 1
    for index, row in df_wait_contact.iterrows():
        print(f'正在打招呼第{n}个')
        print(row['bossName'])
        job_url = row['job_url']
        send_message_to_hr(job_url)
        df.loc[index, 'if_contact'] = '1'
        df.to_csv(data_file, sep='\t', encoding='utf-8-sig', index=False)
        if n == 20:
            break
        n += 1
        time.sleep(random.uniform(1, 10))
    print('打招呼完成，共计打招呼{}个'.format(n))


# 批量自动化-爬取沟通内容
def batch_crawl_dialogue_content():
    data_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
    df = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
    print(df)
    df['if_contact'] = ''
    df_wait_contact = df[df['if_contact'].isnull()]
    print(df_wait_contact)
    n = 1
    for index, row in df_wait_contact.iterrows():
        print(f'正在打招呼第{n}个')
        print(row['bossName'])
        job_url = row['job_url']
        send_message_to_hr(job_url)
        df.loc[index, 'if_contact'] = '1'
        df.to_csv(data_file, sep='\t', encoding='utf-8-sig', index=False)
        if n == 10:
            break
        n += 1
        time.sleep(random.uniform(1, 10))
    print('打招呼完成，共计打招呼{}个'.format(n))


if __name__ == '__main__':
    # keyword = '贷款'
    # search_jobs_links_by_keyword(keyword)
    job_url = 'https://www.zhipin.com/job_detail/1c62cdd42e95a7051HJy2tW0GFJX.html?lid=8Z9W4Yzxbs4.search.141&securityId=CVA3oqIaspdqX-s116geM7-hLLBJNqfycwaMgDKn7iClgmlaSRRf7HfuwZ3RrHfKTC0OJZx49M3EJlFW1Hx0-J0L4WGKQG47IugaISrcnpqYCNz0ku60CcMI5gmHRwu9JywaYvxuNjiKR_a9eMsV4-IO2HX7ZbgPA9A4MpcQDW-oBXg~'
    # send_message_to_hr(job_url)
    # data_file=r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
    # company_filter(data_file)
    batch_send_message()
    # crawl_dialogue_content(job_url)
