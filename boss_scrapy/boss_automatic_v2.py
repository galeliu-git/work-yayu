'''
Author: galeliu
Date: 2024-09-11 12:45:56
LastEditTime: 2024-09-23 10:52:08
LastEditors: galeliu
Description: .
'''
'''
Author: galeliu
Date: 2024-09-09 16:30:13
LastEditTime: 2024-09-11 11:51:23
LastEditors: galeliu
Description: .
'''
# url = "https://www.zhipin.com/"

from DrissionPage import ChromiumPage, WebPage, SessionPage, ChromiumOptions
import time
import csv
import random
import pandas as pd
import os
import schedule
jobs_url_format = 'https://www.zhipin.com/job_detail/{}.html?lid={}1&securityId={}'
consultation_content_list = [
    '你好,不好意思打扰了，我想咨询一下个人做贷款，请问您这边有你们公司贷款业务员的联系方式吗？',
    '打扰了，不好意思，我想做贷款咨询，请问您这边有你们公司贷款业务员的联系方式吗？',
    '抱歉，打扰一下，我想做贷款，能给我介绍一个你们做贷款的人的联系方式吗？',
]
salary_list = ['402', '403', '404', '405', '406', '407']


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
    base_url = "https://www.zhipin.com/web/geek/job?query={}&salary={}"
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
    for salary in salary_list:
        page = ChromiumPage()
        # 监听数据包
        data_path_jobs_info = 'wapi/zpgeek/search/joblist'
        page.listen.start(targets=data_path_jobs_info)
        url = base_url.format(keyword, salary)
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
    # writer_data_info.close()
    print('爬取完成')
    company_filter(data_save_path)


# 与hr打招呼
def send_message_to_hr(job_url):
    # 输入内容
    consultation_content = random.choice(consultation_content_list)
    page = ChromiumPage()
    page.get(job_url)
    # time.sleep(20)
    # 点击立即沟通
    if page.ele('.btn btn-startchat') and page.ele('.btn btn-startchat').text == '立即沟通':
        page.ele('.btn btn-startchat').click()
        time.sleep(random.uniform(1, 2))
        if page.ele('.btn btn-outline btn-cancel'):
            # 点击【留在此页】
            page.ele('.btn btn-outline btn-cancel').click()
        print('打招呼成功')
        return 1
        # # 点击继续沟通
        # if page.ele('.btn btn-startchat').text == '继续沟通':
        #     page.ele('.btn btn-startchat').click()
        #     # 等待页面加载
        #     time.sleep(random.uniform(1, 10))
        #     # 输入内容
        #     page.ele('.chat-input').input(consultation_content)
        #     # 点击发送
        #     # page.ele('@text()=发送').click()
        #     page.ele('.btn-v2 btn-sure-v2 btn-send').click()
        # page.ele('.input-area').input(consultation_content)
    elif page.ele('.btn btn-startchat') and page.ele('.btn btn-startchat').text == '继续沟通':
        page.ele('.btn btn-startchat').click()
        print('继续沟通')
        time.sleep(random.uniform(1, 2))
        if page.ele('.boss-dialog__button button-outline '):
            # 点击【取消】温馨提示
            page.ele('.boss-dialog__button button-outline ').click()
        # 输入内容
        page.ele('.chat-input').input('你好~')
        # 点击发送
        page.ele('.btn-v2 btn-sure-v2 btn-send').click()
        print('打招呼成功')
        return 1
    else:
        print('职位已取消')
        return 2


# 与hr继续沟通
def continue_chat(job_url):
    page = ChromiumPage()
    page.get(job_url)
    # 点击继续沟通
    if page.ele('.btn btn-startchat') and page.ele('.btn btn-startchat').text == '继续沟通':
        page.ele('.btn btn-startchat').click()
        print('判断有无温馨提示')
        if page.ele('.boss-dialog__button button-outline '):
            # 点击【取消】温馨提示
            page.ele('.boss-dialog__button button-outline ').click()
            print('温馨提示已取消')
        # 判断是否双向沟通
        if page.ele('.btn-resume toolbar-btn tooltip tooltip-top unable'):
            print('判断是否打过招呼')
            if not page.ele('.item-myself'):
                # 输入内容
                page.ele('.chat-input').input('你好~')
                # 点击发送
                page.ele('.btn-v2 btn-sure-v2 btn-send').click()
                print('打招呼成功')
            else:
                print('对方未回复')
                return 0
        # # 等待页面加载
        # time.sleep(random.uniform(2, 5))
        # page.wait.load_start()
        # with open('test.txt', 'w', encoding='utf-8') as f:
        #     f.write(page.html)

        # # 接受工作地点
        # if page.ele('.msg-dialog msg-dialog-position') and page.ele('.msg-dialog msg-dialog-position').ele('@text()=可以接受'):
        #     page.ele('.msg-dialog msg-dialog-position').ele('@text()=可以接受').click()
        #     print('已接受工作地点')
        print('判断是否已交换联系方式')
        if page.ele('@text()=请求交换电话已发送') or page.ele('.message-dialog green') or page.ele('.message-card-wrap green'):
            print('已交换过联系方式')
            return 1
        print('检索是否有简历邀请')
        # 接受简历邀请
        if page.ele('.message-dialog boss-green') and page.ele('.message-dialog boss-green').ele('@text()=同意'):
            if 'disabled' in page.ele('.message-dialog boss-green').ele('@text()=同意').attrs['class']:
                pass
            else:
                page.ele('.message-dialog boss-green').ele('@text()=同意').click()
                print('已接受简历邀请')
                # 发送简历术语
                jianli_content = '可以看看我的简历哈，合适的话可以聊聊~'
                # 输入内容
                page.ele('.chat-input').input(jianli_content)
                # 点击发送
                page.ele('.btn-v2 btn-sure-v2 btn-send').click()
        print('检索是否有联系方式邀请')
        # 接受联系方式邀请
        if page.ele('.message-dialog green') and page.ele('.message-dialog green').ele('@text()=同意'):
            if 'disabled' in page.ele('.message-dialog green').ele('@text()=同意').attrs['class']:
                pass
            else:
                page.ele('.message-dialog green').ele('@text()=同意').click()
                # 输入内容
                page.ele('.chat-input').input('好的，有空电话沟通哈')
                # 点击发送
                page.ele('.btn-v2 btn-sure-v2 btn-send').click()
                print('已接受联系方式邀请')
        print('判断是否需要发送简历')
        # 如果没有交换过简历
        if page.ele('@text()=附件简历请求已发送') or page.ele('@text()=我想要一份您的附件简历，您是否同意'):
            print('已交换过简历')
        elif not page.ele('.btn-resume toolbar-btn tooltip tooltip-top unable'):
            # 点击换简历
            if page.ele('.btn-resume toolbar-btn tooltip tooltip-top'):
                page.ele('.btn-resume toolbar-btn tooltip tooltip-top').click()
                if page.ele('.sentence-popover panel-resume').ele('@text()=确定'):
                    page.ele(
                        '.sentence-popover panel-resume').ele('@text()=确定').click()
                    # 输入内容
                    page.ele('.chat-input').input('可以看看我的简历哈，合适的话电话沟通')
                    # 点击发送
                    page.ele('.btn-v2 btn-sure-v2 btn-send').click()
                    print('已发送简历请求')
        else:
            print('对方没有回复')
            return 0
        print('判断是否需要发送联系方式')
        # 如果没有交换过联系方式
        if page.ele('@text()=请求交换电话已发送') or page.ele('.message-dialog green') or page.ele('.message-card-wrap green'):
            print('已交换过联系方式')
        elif not page.ele('.btn-contact toolbar-btn tooltip tooltip-top unable'):
            # 点击换电话
            if page.ele('.btn-contact toolbar-btn tooltip tooltip-top'):
                page.ele('.btn-contact toolbar-btn tooltip tooltip-top').click()
                if page.ele('.sentence-popover panel-contact').ele('@text()=确定'):
                    page.ele(
                        '.sentence-popover panel-contact').ele('@text()=确定').click()
                    # # 输入内容
                    # page.ele('.chat-input').input('有空电话沟通哈')
                    # # 点击发送
                    # page.ele('.btn-v2 btn-sure-v2 btn-send').click()
                    print('已发送交换电话请求')
        else:
            print('对方没有回复')
            return 0
    else:
        print('没有沟通过')
        return 0
    return 1


# 爬取对话内容
def crawl_dialogue_content(url):
    page = ChromiumPage()
    page.get(url)
    dialogue_content = ''
    boss_content = ''
    number = ''
    # 点击【继续沟通】
    if page.ele('.btn btn-startchat') and page.ele('.btn btn-startchat').text == '继续沟通':
        page.ele('.btn btn-startchat').click()
        # 等待页面加载
        time.sleep(random.uniform(1, 10))
        # 获取对话内容
        dialogue_content = page.ele('.im-list').text
        dialogue_content = str(dialogue_content).replace('\n', '\\n')
        # print('所有对话', dialogue_content)
        # 对方对话内容
        boss_content_eles = page.eles('.item-friend')
        if boss_content_eles:
            for boss_ele in boss_content_eles:
                boss_content += boss_ele.text + '\\n'
        boss_content = str(boss_content).replace('\n', '\\n')
        print('对方对话：', boss_content)
        # 判断有无电话信息
        if page.ele('.contact-info-container'):
            number = page.ele('.contact-info-container').page('.number').text
            print('number:', number)
    else:
        print('未沟通过')
    return dialogue_content, boss_content, number


# 批量自动化-打招呼
def batch_send_message():
    data_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
    df = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
    print(df)
    # df['if_contact'] = ''
    df_wait_contact = df[df['if_contact'] == 0]
    print(df_wait_contact)
    print('待打招呼数量：', len(df_wait_contact))
    n = 1
    for index, row in df_wait_contact.iterrows():
        print(f'正在打招呼第{n}个')
        print(row['bossName'])
        job_url = row['job_url']
        res = send_message_to_hr(job_url)
        df.loc[index, 'if_contact'] = res
        df.to_csv(data_file, sep='\t', encoding='utf-8-sig', index=False)
        if n == 50:
            break
        n += 1
        time.sleep(random.uniform(1, 10))
    print('打招呼完成，共计打招呼{}个'.format(n))


# 批量自动化-继续沟通
def batch_continue_contact():
    data_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
    df = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
    # df['if_contact'] = df['if_contact'].astype(str)
    print(df)
    # df['if_continue_contact'] = 0
    df_wait_contact = df[df['if_continue_contact'] == 0]
    df_wait_contact = df_wait_contact[df['if_contact'] == 1]
    print(df_wait_contact)
    print('待继续沟通数量：', len(df_wait_contact))
    n = 0
    for index, row in df_wait_contact.iterrows():
        print(f'正在继续沟通第{n+1}个')
        print(row['bossName'])
        job_url = row['job_url']
        try:
            res = continue_chat(job_url)
            df.loc[index, 'if_continue_contact'] = res
        except Exception as e:
            print(e)
        df.to_csv(data_file, sep='\t', encoding='utf-8-sig', index=False)
        # if n == 20:
        #     break
        n += 1
        time.sleep(random.uniform(1, 10))
    print('共计继续沟通{}个'.format(n))


# 批量自动化-爬取沟通内容
def batch_crawl_dialogue_content():
    data_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
    df = pd.read_csv(data_file, sep='\t', encoding='utf-8-sig')
    print(df)
    # df['if_continue_contact'] = ''
    df_wait_contact = df[df['number'].isnull()]
    df_wait_contact = df_wait_contact[df['if_continue_contact'] == 1]
    print(df_wait_contact)
    n = 1
    for index, row in df_wait_contact.iterrows():
        print(f'正在爬第{n}个')
        print(row['bossName'])
        job_url = row['job_url']
        dialogue_content, boss_content, number = crawl_dialogue_content(
            job_url)
        df.loc[index, 'dialogue_content'] = dialogue_content
        df.loc[index, 'boss_content'] = boss_content
        df.loc[index, 'number'] = number
        df.to_csv(data_file, sep='\t', encoding='utf-8-sig', index=False)
        n += 1
        time.sleep(random.uniform(1, 10))
    print('爬取对话完成，共计爬取{}个'.format(n))


def main():
    print('开始等待可执行任务...')
    # 给boss发打招呼
    schedule.every().day.at('11:00').do(batch_send_message)
    # 与boss继续沟通：换简历、换电话
    schedule.every().day.at('11:20').do(batch_continue_contact)
    # 给boss发打招呼
    schedule.every().day.at('15:05').do(batch_send_message)
    # 与boss继续沟通：换简历、换电话
    schedule.every().day.at('15:40').do(batch_continue_contact)
    # 爬取沟通内容
    schedule.every().day.at('17:00').do(batch_crawl_dialogue_content)
    while True:
        schedule.run_pending()   # 运行所有可以运行的任务
        time.sleep(1)


if __name__ == '__main__':
    keyword = '贷款'
    # search_jobs_links_by_keyword(keyword)
    job_url = 'https://www.zhipin.com/job_detail/13f8301121d7ae5e1XB-2Nm9FFdZ.html?lid=8Z9W4Yzxbs4.search.1161&securityId=7fa6-Sbil2gP9-i1Wd_Ku5NOMH-kXeYqMurBXDzTAndPIEvsRpuiwGUqWj078t7s83Tp1JMWRnMhymMPuMQEwDoL79QcNsetLTJ1W-apyhwxSQ4Sx31XzjaAQBBKZnDMhBxv6qTX0GmS'
    # send_message_to_hr(job_url)
    data_file = r'D:\work\workcode\work-github\work-yayu\boss_scrapy\data\jobs_links_贷款.csv'
    # company_filter(data_file)

    # crawl_dialogue_content(job_url)
    # continue_chat(job_url)
    # batch_continue_contact()
    # main()
    # batch_send_message()
    # batch_continue_contact()
    batch_crawl_dialogue_content()
