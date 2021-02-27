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
        return('True')
    else:
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
    while True:
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

    xx = sum(shuzu)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("===================账号详情===================")
    print('账号ID:',data['id'])
    print('账号昵称:',data['nickName'])
    print('绑定手机号:',data['phoneNum'])
    print('当前有',data['score'],'个星星')
    print('今日获得星星',xx,'个')
    print("=============================================")
# 获取账号信息

def sxx(token):
    
    url = 'http://tiantang.mogencloud.com/api/v1/device_logs?page=1&per_page=200'

    biao = {
        'authorization':token,
    }

    fanhui = requests.get(url=url,headers=biao)

    f = fanhui.json()
    f1 = f['data']
    cv = f1['data']
    cvb = cv[0]
    idc = cvb['device_id']
    score = cvb['can_active_score']
    cvbnm = cvb['daily_at']

    urla = 'http://tiantang.mogencloud.com/api/v1/score_logs?device_id='

    urlb = '&score='

    scoreb = str(score)

    urlc = urla+idc+urlb+scoreb

    requests.post(url=urlc,headers=biao)
    # fc = fb.json()
    # print(fc)
    timeArray = time.localtime(cvbnm)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)

    print("=============================================")
    print('时间:',otherStyleTime)
    print('设备ID:',idc)
    print('获得星星:',score)
    print("=============================================")
# 收星星

def zh(fh):

    if fh == '请求未携带token，无权限访问':
        
        return('未登录')
    elif fh == 'Token malformed':

        return('未登录')
    elif fh == '':
        data = fanhuic['data']
        c = data['phoneNum']
        return c
# 判断请求是否带了token


while True:
    
    b = open("token.txt","r")
    du = b.read()
    b.close()
    url = 'http://tiantang.mogencloud.com/web/api/account/message/loading'
    biao = {
        'authorization':du
    }
    fanhui = requests.post(url=url,headers=biao)
    fanhuic = fanhui.json()
    
    sc = zh(fanhuic['msg'])

    print("=====================选项=====================")
    print("当前登录账号:",sc)
    print("立即登录账号:1")
    print("删除当前账号:2")
    print("查看账号信息:3")
    print('开启自动收取:4')
    print('开启手动收取:5')
    print("=============================================")

    xuan = input('请输入选项后的id:')

    if xuan == '1':
        token1 = token()
        if token1 == 'c':
            print("验证码错误")
        else:
            xq(token1)
            wj = open('token.txt','w')
            wj.write(token1)
            wj.close()
        # 登录
    elif xuan == '2':
        print('您确定删除账号吗?')
        qd = input('请输入yes/no:')
        if qd == 'yes':

            qwe = open('token.txt','w')
            qwe.write('null')
            qwe.close()
            print('已删除')
        elif qd == 'no':
            print('已取消')     
    elif xuan == '3':
        if sc == '未登录':
            print('请登陆账号后再试')
        else:
            xq(du)
    elif xuan == '4':
        if sc == '未登录':
            print('请登陆账号后再试')
        else:
            print('已开启自动收星星')
            print('请勿关闭!')
            print('等待收取中......')
            while True:

                timec = time.strftime("%H:%M:%S", time.localtime())
                if timec == '07:00:00':
                    sxx(du)
    elif xuan == '5':
        if sc == '未登录':
            print('请登陆账号后再试')
        else:
            print('手动收取成功')
            sxx(du)

# 选项界面





