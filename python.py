import requests
import time
def ksox():
    print("=============================================")
    print("==$$===$$===$$$$$======$$$$$$$=====$$====$$==")
    print("==$$==$$===$$===$$====$$=====$$=====$$==$$===")
    print("==$$=$$====$$========$$=======$$=====$$$$====")
    print("==$$$========$$$====$$=========$$=====$$=====")
    print("==$$=$$=========$$===$$=======$$=====$$$$====")
    print("==$$==$$===$$===$$====$$=====$$=====$$==$$===")
    print("==$$===$$===$$$$$======$$$$$$$=====$$====$$==")
    print("=============================================")
    print("甜糖心愿自动收星星")
ksox()

def token():
    url = "http://tiantang.mogencloud.com/web/api/login/code?phone="
    # 登录获取验证码url
    url2 = "http://tiantang.mogencloud.com/web/api/login?phone="
    # 登录url
    phone = input("请输入手机号：")
    url1 = url+phone
    denglu = requests.post(url=url1)
    c = denglu.json()
    c1 = c["msg"]
    if c1 == "请求参数有误":
        print("参数有误")
    else:
        print("验证码发送成功") 
        print("如未收到验证码请检查手机号是否正确!")
        vc = input("请输入验证码：")
        cs = "&authCode="
        url3 = url2+phone+cs+vc
        den = requests.post(url=url3)
        d = den.json()
        msg = d['msg']
        if msg == "验证码错误":
            # print("验证码错误")
            return('c')
        else:
            print("登录成功")
            data = d['data']
            token = data['token']
            return token
#获取token

def sj(token):
    url = 'http://tiantang.mogencloud.com/api/v1/score_logs?page=1&per_page=24'
    # 星星查询记录url
    biao = {
        'authorization':token
    }

    fanhui = requests.get(url=url,headers=biao)

    fanhuic = fanhui.json()
    data = fanhuic['data']
    data2 = data['data'] 
    return data2
# 输出数组data2里的所有内容

def f(sjc):
    timeArray = time.localtime(sjc)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)

    timec = time.strftime("%Y-%m-%d", time.localtime())

    # print(otherStyleTime)
    # print(timec)

    if otherStyleTime == timec:
        # print('yes')
        return('True')
    else:
        # print('no')
        return('False')
# 时间戳与当前时间判断
# 一样输出为True，否者False
# 输入为时间戳

def xq(token):
    url = 'http://tiantang.mogencloud.com/web/api/account/message/loading'
    biao = {
        'authorization':token
    }
    fanhui = requests.post(url=url,headers=biao)
    fanhuic = fanhui.json()

    data = fanhuic['data']
    
    data2 = sj(token)
    shuzu = []
    i = 0
    while 1 == 1:
        daily = data2[i]
        daily_at = daily['daily_at']
        score = daily['score']
        ff = f(daily_at)
        if ff == 'False':        
            break
        else:
            i = i + 1
            shuzu.append(score)
            # print(score)

    xx = shuzu[0] + shuzu[1]

    print("=============================================")
    print('账号ID:',data['id'])
    print('账号昵称:',data['nickName'])
    print('绑定手机号:',data['phoneNum'])
    print('当前有',data['score'],'个星星')
    print('今日获得星星',xx,'个')
    print("=============================================")
# 获取账号信息

token1 = token()

if token1 == 'c':
    print("验证码错误")
else:
    xq(token1)








