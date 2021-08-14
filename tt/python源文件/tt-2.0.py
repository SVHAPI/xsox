import time
import requests
import datetime

# Webhook企业微信机器人key
key = ''

def Webhook(text):
    # Webhook企业微信机器人消息推送
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
    user = requests.post(url=url, json={"msgtype": "markdown","markdown": {"content": text}}, params={'key': key}).json()
    print(user)

def main():
    # 开始自检是否登录
    with open('token.txt', 'r') as tokenn:
        token = tokenn.read()
    url = 'http://tiantang.mogencloud.com/web/api/account/message/loading'
    user = requests.post(url=url, headers={'authorization': token}).json()
    if user['msg'] == '':  # 已登录执行

        #####################收取星星#####################
        url = 'http://tiantang.mogencloud.com/api/v1/device_logs'  # 设备星星查询
        device_logs = requests.get(url=url,headers={'authorization':token}).json()  # 获取设备产生心愿
        scores = device_logs['data']['data']
        for i in scores:
            timeArray = time.localtime(i['daily_at'])  # 时间戳转换
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            timec = time.strftime("%Y-%m-%d", time.localtime())  # 获取当前时间
            dt = datetime.datetime.strptime(timec, "%Y-%m-%d")
            out_date = (dt + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            if otherStyleTime == out_date:
                url = 'http://tiantang.mogencloud.com/api/v1/score_logs'
                requests.post(url=url,headers={'authorization':token}, data={'device_id': i['device_id'], 'score': i['can_active_score']})

        #####################查询星星#####################
        url = 'http://tiantang.mogencloud.com/api/v1/score_logs'  # 所有星星查询
        score_logs = requests.get(url=url,headers={'authorization':token}).json()  # 获取所以心愿记录
        scorelist = score_logs['data']['data']
        xingyuan = 0
        for i in scorelist:
            timec = time.strftime("%Y-%m-%d", time.localtime())  # 获取当前时间
            timeArray = time.localtime(i['daily_at'])  # 时间戳转换
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            if otherStyleTime == timec:  # 等于当前时间的条件执行
                xingyuan = xingyuan + i['score']

        ##################检查是否可以提现#################
        url = 'http://tiantang.mogencloud.com/web/api/account/message/loading'
        user = requests.post(url=url, headers={'authorization': token}).json()
        score = user['data']['score']  # 总星星
        phoneNum = user['data']['phoneNum']  # 账号
        devList = user['data']['devList']  # 总设备
        if score >= 1000:
            tix = '是'
        else:
            tix = '否'

        #####################设备查询#####################
        textt = ''
        for i in devList:
            url = 'http://tiantang.mogencloud.com/api/v1/devices/{}/status'.format(i['devId'])  # 查询设备是否在线
            status = requests.get(url=url,headers={'authorization':token}).json()  # 获取设备状态
            uid = status['data']['dev_id']
            url = 'http://tiantang.mogencloud.com/api/v1/score_logs?device_id={}&type=active'.format(i['devId'])  # 查询设备星愿
            if uid == '':
                active = requests.get(url=url,headers={'authorization':token}).json()  # 获取设备状态
                timec = time.strftime("%Y-%m-%d", time.localtime())  # 获取当前时间
                timeArray = time.localtime(active['data']['data'][0]['daily_at'])  # 时间戳转换
                otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
                if timec == otherStyleTime:
                    textt += '\n>UID：' + i['devId'] + '\n>今日获取星愿：' + str(active['data']['data'][0]['score']) + '\n>已离线!\n--------------'  # 设备离线的
            else:
                active = requests.get(url=url,headers={'authorization':token}).json()  # 获取设备状态
                timec = time.strftime("%Y-%m-%d", time.localtime())  # 获取当前时间
                timeArray = time.localtime(active['data']['data'][0]['daily_at'])  # 时间戳转换
                otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
                if timec == otherStyleTime:
                    textt += '\n>UID：' + i['devId'] + '\n>今日获取星愿：' + str(active['data']['data'][0]['score']) + '\n>在线!\n--------------'  # 设备在线的

        #####################消息推送#####################
        text = '<font color="info">**甜糖自动收星星**</font>\n账号：{}\n时间：{}\n总额：{}\n提现：{}\n今日获得：{}\n设备数量：{}\n######设备信息######'.format(phoneNum,timec,score,tix,xingyuan,len(devList))
        Webhook(text + textt)
    else: # 未登录执行
        print('token已失效！')
        url = "http://tiantang.mogencloud.com/web/api/login/code"  # 获取验证码url
        phone = input("请输入手机号：")
        requests.post(url=url, params={'phone': phone}).json()  # 获取验证码
        while True:
            url = "http://tiantang.mogencloud.com/web/api/login"  # 登录url
            print('如未获取到验证码请检查手机号是否输入正确')
            authCode = input("请输入验证码：")
            msg = requests.post(url=url, params={'phone': phone, 'authCode': authCode}).json()  # 获取token
            if msg['msg'] == "验证码错误":
                print("验证码错误")
            else:
                print("登录成功")
                token = msg['data']['token']
                with open('token.txt', 'w') as tokenn:  # 写入token
                    tokenn.write(token)
                break

# 每n秒执行一次
def timer(n):
    while True:
        print('开始执行')
        main()
        time.sleep(86400)

timer(86400)
