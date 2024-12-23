import json
import lark_oapi as lark
from lark_oapi.api.calendar.v4 import *
import requests
from flask import Flask, request, redirect, session

app = Flask(__name__)
app_id = "cli_a7ed07ffb379500d"
app_secret = "2hf5uNFPFXdi7gXSTsWqTGabZGmYpYJP"


# email_info={"subject": email["subject"], "content": content, "begin_time": res_json["begin_time"], "end_time": res_json["end_time"], "link": res_json["link"]}

# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 以下示例代码是根据 API 调试台参数自动生成，如果存在代码问题，请在 API 调试台填上相关必要参数后再使用

@app.route("/callback")
def callback():
    response = requests.post(url="https://open.feishu.cn/open-apis/authen/v2/oauth/token", data={
        "grant_type": "authorization_code",
        "client_id": app_id,
        "client_secret": app_secret,
        "redirect_uri": "http://localhost:8080/callback",
        "code": request.args.get("code"),
    })

    session["user_access_token"] = response.json()["access_token"]
    session["refresh_access_token"] = response.json()["refresh_token"]
    return session["user_access_token"]


def get_user_access_token():
    refresh_access_token = session.get("user_access_token")
    if not refresh_access_token:
        # 跳转到登录页面
        return redirect(
            location=f"https://accounts.feishu.cn/open-apis/authen/v1/authorize?client_id={app_id}&redirect_uri=http://localhost:8080/callback&scope=offline_access calendar:calendar.event:create calendar:calendar:readonly")
    else:
        response = requests.post(url="https://open.feishu.cn/open-apis/authen/v2/oauth/token", data={
            "grant_type": "refresh_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "refresh_token": refresh_access_token,
        })

        session["user_access_token"] = response.json()["access_token"]
        session["refresh_access_token"] = response.json()["refresh_token"]
        return session["user_access_token"]


def get_calendar_id():
    calendar_id = session.get("calendar_id")
    if calendar_id:
        return calendar_id

    # 创建client
    client = lark.Client.builder() \
        .enable_set_token(True) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: PrimaryCalendarRequest = PrimaryCalendarRequest.builder() \
        .user_id_type("open_id") \
        .build()

    # 发起请求
    user_access_token = get_user_access_token()
    option = lark.RequestOption.builder().user_access_token(user_access_token).build()
    response: PrimaryCalendarResponse = client.calendar.v4.calendar.primary(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.calendar.v4.calendar.primary failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return "error"

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    session["calendar_id"] = str(response.data.calendars[0].calendar.calendar_id)
    return session["calendar_id"]


def calendar_append(email_info):
    # 创建client
    # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token

    user_access_token = get_user_access_token()
    calendar_id = get_calendar_id()

    client = lark.Client.builder() \
        .enable_set_token(True) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateCalendarEventRequest = CreateCalendarEventRequest.builder() \
        .calendar_id(calendar_id) \
        .user_id_type("user_id") \
        .request_body(CalendarEvent.builder()
                      .summary(email_info["subject"])
                      .description(email_info["job_description"])
                      .start_time(TimeInfo.builder()
                                  .timestamp(str(email_info["begin_time"]))
                                  .timezone("Asia/Shanghai")
                                  .build())
                      .end_time(TimeInfo.builder()
                                .timestamp(str(email_info["end_time"]))
                                .timezone("Asia/Shanghai")
                                .build())
                      .vchat(Vchat.builder()
                             .vc_type("third_party")
                             .icon_type("vc")
                             .description("链接link")
                             .meeting_url(email_info["link"])
                             .build())
                      .build()) \
        .build()

    # 发起请求
    option = lark.RequestOption.builder().user_access_token(user_access_token).build()
    response: CreateCalendarEventResponse = client.calendar.v4.calendar_event.create(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.calendar.v4.calendar_event.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    calendar_append()
