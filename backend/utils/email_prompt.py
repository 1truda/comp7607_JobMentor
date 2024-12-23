from datetime import datetime

def get_email_time_prompt(message):

    chats = [
        {"role": "system", "content": "Your task is to extract time information from the message, then output the absolute time information and judge the time describe the past or future \
         Use the format <> to highlight your output. If there is more than one time information in the message, you should output all of them and separate them in ','. For example, if the \
         time information is a week ago, you should output <past:a week>."},
        {"role": "user", "content": "Add the interview arrangement from emails received from last week to the calendar."},
        {"role": "assistant", "content": "<past:a week>"},
        {"role": "user", "content": "Add the interview arrangement that will happen by 10:00 tonight from emails to the calendar."},
        {"role": "assistant", "content": "<future:10:00 tonight>"},
        {"role": "user", "content": message}
    ]

    return chats

def get_time_convert_prompt(message):

    chats = [
        {"role": "system", "content": f"Your task is to convert the time information into seconds. You may receive a time span or a specific time.\
         If it is a time span, you should output the total seconds. If it is a specific time, you should output the seconds from the current time({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}). \
         Output your reasoning process and use the format <> to highlight your output. For example, if the time information is a week, you should output <604800>"},
        {"role": "user", "content": message}
    ]

    return chats

def get_email_extract_prompt(message):

    chats = [
        {"role": "system", "content": "You will receive an interview invitation email. Your task is to extract the interview meeting link,Job description, the begin time and the end time of the interview. \
         If you do not know the end time, you can assume it is 1 hour after the begin time. The begin time and the end time should be fommated as 'YYYY-MM-DD HH:MM'. \
         If you do not know the Job description, you can assign the value \"unknown\" to it.\
         Use the format {'link': 'link', 'begin_time': 'begin_time', 'end_time': 'end_time'} to highlight your output. \
         For example, if the interview meeting link is 'https://meet.google.com/abcde' and the begin time is '2024-01-01 10:00'\
         you should output {'link': 'https://meet.google.com/abcde', 'job_description': 'unknown', 'begin_time': '2024-01-01 10:00', 'end_time': '2024-01-01 11:00'}"},
         {"role": "user", "content": message}
    ]

    return chats