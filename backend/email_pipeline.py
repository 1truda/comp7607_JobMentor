from utils.llm import *
from utils.calender_manage import *
from utils.mail import GmailUtils
import utils.email_prompt as email_prompt
import re
from datetime import datetime, timedelta
import time
import concurrent.futures as cf
import json

# 包管理问题看 https://islishude.github.io/blog/2019/06/29/python/Python%E6%A8%A1%E5%9D%97%E5%92%8C%E5%8C%85%E7%AE%A1%E7%90%86/
thread_pool_size = 3
thread_pool = cf.ThreadPoolExecutor(thread_pool_size)
email_utils = GmailUtils('utils/token.json', 'utils/credentials.json')


def email_pipeline_impl(command):
    model = model_factory("Doubao")

    # 调用模型提取时间信息
    time_info_str = model.chat_completion(email_prompt.get_email_time_prompt(command))
    print(f'-------------\nllm output1: time range\n{time_info_str}\n')
    time_raw_info_dict = extract_time_info(time_info_str)
    timestamp_dict = {}

    for key, value in time_raw_info_dict.items():
        time_value = model.chat_completion(email_prompt.get_time_convert_prompt(value))
        time_value_seconds = extract_time_value(time_value)
        now = datetime.now()
        if key == "past":
            timestamp_dict[key] = int(round((now - timedelta(seconds=time_value_seconds)).timestamp()))
        elif key == "future":
            timestamp_dict[key] = int(round((now + timedelta(seconds=time_value_seconds)).timestamp()))

    # print(timestamp_dict)
    if "past" not in timestamp_dict:
        timestamp_dict["past"] = int(round((datetime.now() - timedelta(days=7)).timestamp()))
    if "future" not in timestamp_dict:
        timestamp_dict["future"] = int(round((datetime.now() + timedelta(days=7)).timestamp()))

    # 调用email api获取邮件id列表
    email_ids = email_utils.get_messages_list(q="interview") + email_utils.get_messages_list(
        q="test") + email_utils.get_messages_list(q="exam")
    str_email_ids = []
    for email_id in email_ids:
        str_email_ids.append(json.dumps(email_id))
    str_email_ids = set(str_email_ids)
    email_ids = []
    for i in str_email_ids:
        email_ids.append(json.loads(i))
    # print(email_ids)

    # 多线程调用email api获取邮件内容，筛选符合时间范围的邮件
    email_content_futures = []
    for i in range(thread_pool_size):
        n = len(email_ids)
        task_size = n // thread_pool_size
        email_ids_ = email_ids[task_size * i:] if i == thread_pool_size - 1 else email_ids[
                                                                                 task_size * i: task_size * (i + 1)]
        email_content_futures.append(thread_pool.submit(filter_emails, email_ids_, timestamp_dict))

    filtered_emails = []
    for future in email_content_futures:
        sub_filtered_emails = future.result()
        filtered_emails += sub_filtered_emails

    # 多线程调用模型提取邮件信息
    if len(filtered_emails) > 0:
        email_info_futures = []
        for i in range(thread_pool_size):
            n = len(filtered_emails)
            task_size = n // thread_pool_size
            filtered_emails_ = filtered_emails[task_size * i:] if i == thread_pool_size - 1 else filtered_emails[
                                                                                                 task_size * i: task_size * (
                                                                                                             i + 1)]
            email_info_futures.append(thread_pool.submit(extract_email_info, filtered_emails_, timestamp_dict, model))

        extracted_emails = []
        for future in email_info_futures:
            sub_extracted_emails = future.result()
            extracted_emails += sub_extracted_emails
    # print(extracted_emails)

    # 调用日程管理api添加日程
    for email in extracted_emails:
        if email:
            calendar_append(email)


def extract_time_info(time_info_str):
    try:
        res = {}
        time_info = time_info_str.split(",")
        for i in range(len(time_info)):
            extract_str = re.findall(r"<(.*)>", time_info[i])[0]
            extract_str = extract_str[1:-1]
            extract_str_list = extract_str.split(":")
            if len(extract_str_list) == 2:
                res[extract_str_list[0]] = extract_str_list[1]
            else:
                res[extract_str_list[0]] = "a day"

        return res
    except Exception as e:
        print(e)
        return {"past": "a day"}


def extract_time_value(time_value_str):
    try:
        extract_str = re.findall(r"<(.*)>", time_value_str)[0]
        extract_str = extract_str[1:-1]
        return int(extract_str)
    except Exception as e:
        print(e)
        return 86400


def filter_emails(email_ids, timestamp_dict):
    filtered_emails = []
    for email_id in email_ids:
        subject, content, timestamp = email_utils.get_message_with_subject_and_time(email_id['id'])
        if int(timestamp) >= timestamp_dict["past"]:
            filtered_emails.append({"subject": subject, "content": content})

    return filtered_emails


def extract_email_info(emails, timestamp_dict, model):
    emails_extracted = []

    for email in emails:
        content = email["content"]
        title = email["subject"]
        print(f'-------------\n{title}\n')
        res = model.chat_completion(email_prompt.get_email_extract_prompt(content))
        print(f'-------------\nllm output2:\n{res}\n')
        res = re.findall(r"{.*}", res)[0]
        try:
            res_json = json.loads(res)
            begin_time_str = res_json["begin_time"]
            begin_time = datetime.strptime(begin_time_str, "%Y-%m-%d %H:%M")
            begin_time_timestamp = int(round(begin_time.timestamp()))

            end_time_str = res_json["end_time"]
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")
            end_time_timestamp = int(round(end_time.timestamp()))

            if begin_time_timestamp <= timestamp_dict["future"]:
                emails_extracted.append(
                    {"subject": email["subject"], "content": content, "job_description": res_json["job_description"],
                     "begin_time": begin_time_timestamp, "end_time": end_time_timestamp, "link": res_json["link"]})
        except:
            # TODO 错误处理
            continue

    return emails_extracted


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = "Add the interview arrangement from emails received this year to the calendar."
    email_pipeline_impl(command)