'''
Author: galeliu
Date: 2024-09-09 16:30:13
LastEditTime: 2024-09-24 17:28:25
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
shangwu_conditions_and = ['商务']
shangwu_conditions_or = ['经理助理', '董事长助理', '总助']


def if_and(and_list, text):
    for item in and_list:
        if item not in text:
            return False
    return True


def if_or(or_list, text):
    for item in or_list:
        if item in text:
            return True
    return False


# 筛选目标候选人--自动化沟通
def send_message_to_seeker():
    base_url = "https://www.zhipin.com/web/chat/recommend"
    data_save_path = 'data/hr/shangwu_chat.csv'
    if os.path.exists(data_save_path):
        # df_comment_info = pd.read_csv(
        #     data_save_path, sep='\t', encoding='utf-8-sig')
        # video_list_crawled = list(set(df_comment_info['video_url'].tolist()))
        writer_data_info = csv.writer(
            open(data_save_path, 'a', newline='', encoding='utf-8-sig'), delimiter='\t')
    else:
        columns_list = ['name',  'experience',]
        writer_data_info = csv.writer(
            open(data_save_path, 'a', newline='',  encoding='utf-8-sig'), delimiter='\t')
        writer_data_info.writerow(columns_list)
    page = ChromiumPage()
    page.get(base_url)
    time.sleep(random.uniform(2, 5))
    # 选择招聘职位
    if page.ele('.icon-arrow svg-icon'):
        page.ele('.icon-arrow svg-icon').click()
        # 选择职位
        job_list_eles = page.ele('.job-list').eles('@tag()=li')
        taget_job = job_list_eles[0].click()

    time.sleep(random.uniform(2, 5))
    n = 0
    m = 1
    page.listen.start()
    while True:
        print(f'正在爬取第{n+1}个，已打招呼{m}个')
        page.listen.wait_silent()
        # 候选人list
        seeker_list_eles = page.ele('.card-list').eles('@tag()=li')
        # print('seeker_list_eles', seeker_list_eles)
        seeker_ele = seeker_list_eles[n]
        print('seeker_ele', seeker_ele.ele('.name').text)
        n += 1
        # 点击候选人卡片
        seeker_ele.ele('.name').click()
        time.sleep(random.uniform(1, 5))
        # 候选人详情元素
        seeker_detail_ele = page.ele('.resume-item-pop-box')
        seeker_resume_text = ''
        # 候选人名字
        name = seeker_detail_ele.ele('.geek-name').text
        print('候选人名字：', name)
        print('判断候选人性别')
        if seeker_detail_ele.ele('.icon-gender iboss-icon_women'):
            print('候选人性别为女')
        else:
            print('候选人性别为男')
            # 关闭职位详情
            if page.ele('.iboss-iconguanbi'):
                page.ele('.iboss-iconguanbi').click()
            continue
        seeker_resume_base_text = ''
        seeker_resume_base_ele = seeker_detail_ele.ele(
            '.resume-item item-base')
        if seeker_resume_base_ele:
            seeker_resume_base_text += seeker_resume_base_ele.text
        resume_item_text = ''
        resume_item_eles = seeker_detail_ele.eles('.resume-item')
        if resume_item_eles:
            for resume_item_ele in resume_item_eles:
                resume_item_text += resume_item_ele.text
        resume_station_eles = seeker_detail_ele.eles(
            '.resume-item resume-station')
        resume_station_text = ''
        if resume_station_eles:
            for resume_station_ele in resume_station_eles:
                resume_station_text += resume_station_ele.text
        resume_summary_eles = seeker_detail_ele.eles('.resume-summary')
        resume_summary_text = ''
        if resume_summary_eles:
            for resume_summary_ele in resume_summary_eles:
                resume_summary_text += resume_summary_ele.text
        seeker_resume_text = seeker_resume_base_text + resume_item_text + \
            resume_station_text + resume_summary_text
        # 判断候选人是否满足筛选条件
        if if_and(shangwu_conditions_and, seeker_resume_text):
            print('候选人满足and条件')
        else:
            print('候选人不满足and条件')
            # 关闭职位详情
            if page.ele('.iboss-iconguanbi'):
                page.ele('.iboss-iconguanbi').click()
            continue
        if if_or(shangwu_conditions_or, seeker_resume_text):
            print('候选人满足or条件')
        else:
            print('候选人不满足or条件')
            # 关闭职位详情
            if page.ele('.iboss-iconguanbi'):
                page.ele('.iboss-iconguanbi').click()
            continue
        # 与候选人打招呼
        # print(seeker_detail_ele.html)
        if seeker_detail_ele.ele('.btn btn-greet') and seeker_detail_ele.ele('.btn btn-greet').text == '打招呼':
            # print(seeker_detail_ele.ele('btn btn-greet').text)
            seeker_detail_ele.ele('.btn btn-greet').click()
            print('打招呼成功')
            # 获取候选人经历概览
            experience = resume_summary_text
            # 写入数据
            writer_data_info.writerow(
                [name, experience])
        else:
            print('不能打招呼')
        # page.listen.start()
        # 关闭职位详情
        if page.ele('.iboss-iconguanbi'):
            page.ele('.iboss-iconguanbi').click()
        if m >= 20:
            break
        m += 1
        time.sleep(random.uniform(2, 5))
        # break

    # # 关闭page
    # page.quit()
    print('打招呼完成')


if __name__ == '__main__':
    send_message_to_seeker()
