from DrissionPage import ChromiumPage, WebPage, SessionPage, ChromiumOptions
import time
import csv
import random
import pandas as pd
import os
# from fake_useragent import UserAgent
# 实例化一个对象
# ua = UserAgent()
# co = ChromiumOptions().headless()
co = ChromiumOptions()


# cookies = 'name1=value1; name2=value2; path=/; domain=.example.com;'

# page = ChromiumPage()
# page.set.cookies(cookies)
def data_list_duplicate(data_list):
    return_list = []
    duplicat_list = []
    for i in data_list:
        if i['cid'] not in duplicat_list:
            duplicat_list.append(i['cid'])
            return_list.append(i)
    return return_list


# 获取视频信息
def craw_video_info_by_url(url):
    # 隐藏浏览器
    # co.headless(on_off=True)
    # 随机useragent
    # random_ua = ua.random
    # print(random_ua)
    # co.set_user_agent(user_agent=random_ua)
    page = ChromiumPage(co)
    # page = SessionPage()
    # 监听数据包
    data_path_video_info = 'aweme/v1/web/aweme/detail/'
    # data_path_comment_info = 'aweme/v1/web/comment/list/'
    page.listen.start(targets=data_path_video_info)
    page.get(url)
    # print(page.mode)
    # 等待数据包加载
    resp = page.listen.wait(timeout=10)
    # print(len(resp))
    # open('test.txt','w',encoding='utf-8').write(str(resp))
    # 解析视频信息
    # print(resp.url)
    video_info_json_data = resp.response.body
    # print(video_info_json_data)
    # 标题
    title = video_info_json_data['aweme_detail']['desc']
    # print('title',title)
    # 发布人
    author = video_info_json_data['aweme_detail']['author']['nickname']
    # print('author',author)
    # 发布时间
    publish_time = video_info_json_data['aweme_detail']['create_time']
    # 时间戳转时间
    publish_time = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(publish_time))
    # print('publish_time',publish_time)
    # 评论数
    comment_count = video_info_json_data['aweme_detail']['statistics']['comment_count']
    # print('comment_count',comment_count)
    # 点赞数
    digg_count = video_info_json_data['aweme_detail']['statistics']['digg_count']
    # print('digg_count',digg_count)
    # 收藏数
    collect_count = video_info_json_data['aweme_detail']['statistics']['collect_count']
    # print('collect_count',collect_count)
    data_dict = {
        'url': url,
        'title': title,
        'author': author,
        'publish_time': publish_time,
        'comment_count': comment_count,
        'digg_count': digg_count,
        'collect_count': collect_count
    }
    time.sleep(random.uniform(2, 5))
    # 关闭page
    page.quit()
    return data_dict


# 获取评论信息
def craw_comment_info_by_url(url):
    # 隐藏浏览器
    # co.headless(on_off=True)
    # 随机useragent
    # random_ua = ua.random
    # print(random_ua)
    # co.set_user_agent(user_agent=random_ua)
    page = ChromiumPage(co)
    data_path_comment_info = 'aweme/v1/web/comment/list'
    data_path_list = ['aweme/v1/web/comment/list',
                      'aweme/v1/web/comment/list/reply/']
    page.listen.start(targets=data_path_list)
    page.get(url)
    # 点击评论按钮
    page.ele('._MqDc0AY').ele('.LMSJtzvq').ele('评论').click()
    # print(page.mode)
    # page.ele('@text()=评论').click()
    comment_data_list = []
    i = 0
    # while True:
    for i in range(100):
        time.sleep(random.uniform(1, 3))
        i += 1
        # print('正在加载第{}次'.format(i))
        # 循环点击展开评论
        comments_list = []
        while True:
            try:
                time.sleep(random.uniform(0.5, 1))
                # page.ele('._MqDc0AY').ele('text^展开').click()
                page.ele('._MqDc0AY').ele('@@tag()=span@@text()^展开').click()
                resp = page.listen.wait(timeout=10)
                if resp is False:
                    pass
                else:
                    comments_list += resp.response.body['comments']
            except:
                # print('展开评论失败')
                break
        # 下滑加载页面数据
        page.scroll.to_bottom()
        # # 评论滑块滚动到最底部
        # page.ele('._MqDc0AY').ele('@data-e2e=comment-list').scroll.to_bottom()

        resp = page.listen.wait(timeout=10)
        # 如果加载超时，代表没有更多数据了，退出循环
        # if resp is False:
        #     break
        if resp is False:
            pass
        else:
            comments_list += resp.response.body['comments']
        # 等待数据包加载
        while True:
            resp = page.listen.wait(timeout=10)
            if resp is False:
                break
            comments_list += resp.response.body['comments']
            # print(1)
            # print(resp.response.body['comments'])
        # print(resp)
        # print(resp.url)
        # 解析评论信息
        # comment_info_json_data = resp.response.body
        # print(comment_info_json_data)
        # print(comment_info_json_data['comments'][:15])
        for comment in comments_list:
            # 评论人
            comment_user = comment['user']['nickname']
            # print('comment_user',comment_user)
            # 评论内容
            comment_text = comment['text']
            # print('comment_text',comment_text)
            # 评论时间
            comment_time = comment['create_time']
            comment_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(comment_time))
            # print('comment_time',comment_time)
            # 评论地点
            # comment_location = comment['ip_label']
            comment_location = '无'
            # print('comment_location',comment_location)
            # 评论人个人页面链接
            sec_uid = comment['user']['sec_uid']
            # short_id = comment['user']['short_id']
            unique_id = comment['user']['unique_id']
            if unique_id:
                short_id = unique_id
            else:
                short_id = comment['user']['short_id']
            cid = comment['cid']
            reply_id = comment['reply_id']
            comment_user_url = 'https://www.douyin.com/user/{}'.format(sec_uid)
            # print('comment_user_url',comment_user_url)
            comment_data_dict = {
                'comment_user': comment_user,
                'comment_text': comment_text,
                'comment_time': comment_time,
                'comment_location': comment_location,
                'comment_user_url': comment_user_url,
                'cid': cid,
                'reply_id': reply_id,
                'short_id': short_id,
            }
            comment_data_list.append(comment_data_dict)
            # print(comment_data_dict)
        try:
            page.ele('._MqDc0AY').ele('暂时没有更多评论')
            break
        except:
            pass
    # print(comment_data_list)
    # page.close()
    # 去重
    # comment_data_list = list(set(comment_data_list))
    res_list = data_list_duplicate(comment_data_list)
    print('共{}条评论,去重后{}条'.format(len(comment_data_list), len(res_list)))
    return res_list


# 爬取视频列表-关键词
def craw_video_list_by_keyword(keyword, save_url_path):
    # save_url_path = r'video_url_{}.txt'.format(keyword)
    url = r'https://www.douyin.com/search/{}?type=video'.format(keyword)
    print(url)
    page = WebPage()
    # page = SessionPage()
    # 监听数据包
    data_path = 'aweme/v1/web/search/item/'
    # data_path_comment_info = 'aweme/v1/web/comment/list/'
    page.listen.start(targets=data_path)
    page.get(url)
    # print(page.mode)
    open(save_url_path, 'w', encoding='utf-8').close
    f_save = open(save_url_path, 'a', encoding='utf-8')
    video_url_list = []
    i = 0
    while True:
        time.sleep(1)
        i += 1
        print('正在加载第{}次'.format(i))
        # 下滑加载页面数据
        page.scroll.to_bottom()
        # 等待数据包加载
        resp = page.listen.wait(timeout=5)
        # 如果加载超时，代表没有更多数据了，退出循环
        if resp is False:
            break
        # print(resp.url)
        # 解析数据
        json_data = resp.response.body
        for item in json_data['data']:
            aweme_id = item['aweme_info']['aweme_id']
            video_url = 'https://www.douyin.com/video/{}'.format(aweme_id)
            video_url_list.append(video_url)
            f_save.write(video_url+'\n')
    # print(video_url_list)
    # print(len(video_url_list))
    f_save.close()
    return video_url_list


def main_video_info():
    keyword = '背债'
    save_url_path = r'video_url_{}.txt'.format(keyword)
    # 视频信息存储路径
    video_info_path = r'video_info_{}.csv'.format(keyword)
    df_video_info = pd.read_csv(video_info_path, sep='\t', encoding='utf-8')
    video_list_crawled = df_video_info['url'].tolist()
    writer_video_info = csv.writer(
        open(video_info_path, 'a', newline='', encoding='utf-8'), delimiter='\t')
    video_info_columns = ['url', 'title', 'author', 'publish_time',
                          'comment_count', 'digg_count', 'collect_count']
    # writer_video_info.writerow(video_info_columns)
    error_file = 'error.txt'
    error_list = [i.strip()
                  for i in open(error_file, 'r', encoding='utf-8').readlines()]
    with open(save_url_path, 'r', encoding='utf-8') as f:
        url_list = f.readlines()
        for n, url in enumerate(url_list):
            url = url.strip()
            print('开始爬取第{}个视频'.format(n+1))
            print(url)
            try:
                if url in video_list_crawled or url in error_list:
                    print('该视频已经爬取过')
                    continue
                # 根据url爬取 视频信息
                video_info_data_dict = craw_video_info_by_url(url)
                # 视频信息写入csv文件
                video_info_list = [
                    video_info_data_dict['url'],
                    video_info_data_dict['title'],
                    video_info_data_dict['author'],
                    video_info_data_dict['publish_time'],
                    video_info_data_dict['comment_count'],
                    video_info_data_dict['digg_count'],
                    video_info_data_dict['collect_count']
                ]
                writer_video_info.writerow(video_info_list)
                # print('视频信息爬取完成')
                time.sleep(random.uniform(1, 10))
            except Exception as e:
                with open('error.txt', 'a', encoding='utf-8') as f_err:
                    f_err.write(url+'\n')
                # print(url)
                print('爬取失败')
                print(e)
                # break
            # break
    print('视频信息爬取完成')
    return


def main_comment_info(keyword):
    # keyword = '代持'
    save_url_path = r'data/video_url_{}.txt'.format(keyword)
    # save_url_path = r'data/test.txt'
    # 评论信息存储路径
    comment_info_path = r'data/comment_info_{}.csv'.format(keyword)
    video_list_crawled = []
    if os.path.exists(comment_info_path):
        df_comment_info = pd.read_csv(
            comment_info_path, sep='\t', encoding='utf-8')
        video_list_crawled = list(set(df_comment_info['video_url'].tolist()))
        writer_comment_info = csv.writer(
            open(comment_info_path, 'a', newline='', encoding='utf-8'), delimiter='\t')
    else:
        comment_info_columns = ['video_url', 'comment_user',
                                'comment_text', 'comment_time', 'comment_location', 'comment_user_url', 'cid', 'reply_id', 'short_id']
        writer_comment_info = csv.writer(
            open(comment_info_path, 'a', newline='', encoding='utf-8'), delimiter='\t')
        writer_comment_info.writerow(comment_info_columns)
    # video_list_crawled = []
    error_file = 'error.txt'
    error_list = [i.strip()
                  for i in open(error_file, 'r', encoding='utf-8').readlines()]
    with open(save_url_path, 'r', encoding='utf-8') as f:
        url_list = f.readlines()
        for n, url in enumerate(url_list):
            url = url.strip()
            print('开始爬取第{}个视频'.format(n+1))
            print(url)
            try:
                if url in video_list_crawled or url in error_list:
                    print('该视频已经爬取过')
                    continue
                # 根据url爬取 评论信息
                comment_info_data_list = craw_comment_info_by_url(url)
                # print('共有{}条评论'.format(len(comment_info_data_list)))
                for comment_info in comment_info_data_list:
                    # 评论信息写入csv文件
                    comment_info_list = [
                        url,
                        comment_info['comment_user'],
                        comment_info['comment_text'],
                        comment_info['comment_time'],
                        comment_info['comment_location'],
                        comment_info['comment_user_url'],
                        comment_info['cid'],
                        comment_info['reply_id'],
                        comment_info['short_id'],
                    ]
                    writer_comment_info.writerow(comment_info_list)
                time.sleep(random.uniform(1, 5))
            except Exception as e:
                with open('error.txt', 'a', encoding='utf-8') as f_err:
                    f_err.write(url+'\n')
                # print(url)
                print('爬取失败')
                print(e)
                # break
            # break
    return


def main():
    keyword = '背债'
    save_url_path = r'video_url_{}.txt'.format(keyword)
    # # 根据关键词爬取视频url
    craw_video_list_by_keyword(keyword, save_url_path)
    # 根据视频url爬取视频信息
    main_video_info()
    # 根据视频url爬取评论信息
    main_comment_info()


if __name__ == '__main__':
    url = 'https://www.douyin.com/video/7253849203938544896'
    # url = 'https://www.douyin.com/video/7333182883349269769'
    # print(craw_video_info_by_url(url))
    # print()
    # craw_comment_info_by_url(url)
    keyword = '撸贷'
    # save_url_path = r'data/video_url_{}.txt'.format(keyword)
    # craw_video_list_by_keyword(keyword, save_url_path)
    # main()
    # main_video_info()
    main_comment_info(keyword)
