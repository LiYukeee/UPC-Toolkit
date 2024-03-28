"""
本脚本诞生的原因：
校园网络存在问题：
有线网络：延迟低，速度快，但是使用代理有很大问题，适合打游戏或者看视频
无线网络：延迟高，速度慢，使用代理没有问题，适合学习、搜集资料
因此需要拔插网线以获得最优的体验
为将网络认证操作自动化，本脚本应运而生
"""
import winreg
from time import sleep
from requests import post
from win11toast import toast
import time
import json
import psutil


def checkProxy():
    """
    检测当前系统代理状态
    :return: True or False
    """
    try:
        internet_settings = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                           r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
        proxy_enable = winreg.QueryValueEx(internet_settings, 'ProxyEnable')[0]
        winreg.CloseKey(internet_settings)

        if proxy_enable == 1:
            return True
        else:
            return False
    except Exception as e:
        print("无法读取代理配置信息:", e)
        return False


def systemProxy(open_or_close, host='127.0.0.1', port=7890):
    """
    修改系统代理函数
    :param open_or_close: 是否开启 bool
    :param host: IP
    :param port: 端口
    :return:
    """
    proxy = f"{host}:{port}"
    root = winreg.HKEY_CURRENT_USER
    proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    kv_Enable = [
        (proxy_path, "ProxyEnable", 1, winreg.REG_DWORD),
        (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]

    kv_Disable = [
        (proxy_path, "ProxyEnable", 0, winreg.REG_DWORD),
        # (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]
    if open_or_close:
        kv = kv_Enable
    else:
        kv = kv_Disable
    for keypath, value_name, value, value_type in kv:
        hKey = winreg.CreateKey(root, keypath)
        winreg.SetValueEx(hKey, value_name, 0, value_type, value)


# def windows10Note(title, msg, icon_path=None, duration=100, threaded=False):
#     try:
#         toast = ToastNotifier()
#         toast.show_toast(title=title, msg=msg,
#                          icon_path=icon_path,
#                          duration=duration, threaded=threaded)
#     except:
#         a = 1

def windows11Note(title='', msg='', icoPath='C:\\Users\\LiYuke\\OneDrive\\图片\\头像\\245.png'):
    """
    通知函数
    :param title:
    :param msg:
    :param icoPath:
    :return:
    """
    image = {
        'src': icoPath,
        'placement': 'hero'
    }

    toast(title, msg, image=image)


def connect(account, password, service):
    """
    网络认证
    :param account:
    :param password:
    :param service:
    :return:
    """
    currentProxyStatus = checkProxy()
    # ---------0---------
    # 关闭系统代理
    # 在有代理情况下无法完成登录
    if checkProxy():
        systemProxy(False)
    # ---------1---------
    # 登录信息
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Origin": "http://lan.upc.edu.cn",
        "Host": "lan.upc.edu.cn",
    }
    serviceChoice = service  # 选择服务：cmcc(中国移动) ctcc(中国电信) cucc(中国联通) default（校园网）
    if serviceChoice == "ctcc":
        msg = '中国电信'
    elif serviceChoice == 'cmcc':
        msg = '中国移动'
    elif serviceChoice == 'cucc':
        msg = '中国联通'
    elif serviceChoice == 'default':
        msg = '校园网'
    else:
        msg = '其他'
    data = """userId={}&password={}&service={}&queryString=wlanuserip%253D121.249.158.235%2526wlanacname%253D%2526nasip%253D172.22.242.21%2526wlanparameter%253D08-26-ae-33-e4-70%2526url%253Dhttp%253A%252F%252Fwww.google.com%252F%2526userlocation%253Dethtrunk%252F62%253A1667.27&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false"""
    data = data.format(account, password, serviceChoice)
    res = ''
    i = 0
    tryTimes = 1
    icoPath = r"D:/MEDIA/icon/图标.png"
    # ---------2---------
    # 登录
    errnoMessage = ''
    success = False
    for i in range(tryTimes):
        try:
            re = post('http://lan.upc.edu.cn/eportal/InterFace.do?method=login',
                      headers=header, data=data, proxies=None)
            res = re.text
            errnoMessage = json.loads(res)['message'].encode('latin1').decode('utf-8')
            if 'success' in res:
                success = True
                print("登录成功")
                windows11Note('网络认证成功', msg + "网络已连接\n" + errnoMessage)
                if currentProxyStatus:  # 如果原先系统代理是打开状态
                    systemProxy(True)
                return True
        except:
            a = 1
        print("登录第{}次失败".format(i + 1))
        sleep(1)

    if i == tryTimes - 1 and success == False:
        print("登录失败")
        windows11Note('登录网络失败', errnoMessage)
        if currentProxyStatus:  # 如果原先系统代理是打开状态
            systemProxy(True)
        return False
    # print("程序运行结束")
    # 启动其他脚本，在网络登录之后
    # import os
    # os.system('python "C:\\Users\\Script\\sock获取免费流量.py"')


def main():
    """
    我的电脑，通过type-C拓展坞网络接口是“以太网2”，需要判断此项之后的isup状态
    """
    account = '2009050216'
    password = '20020528lyk'
    service = 'ctcc'  # 中国电信
    lanNetStatus = False  # 有线网络连接状态
    netCable = False
    while True:
        interfaces = psutil.net_if_stats()
        eth2 = interfaces['以太网 2']
        # 网线接口判断
        if netCable != eth2.isup:
            if eth2.isup:
                windows11Note('有线网络接入，开始进行认证', '', '')
            else:
                windows11Note('有线网络连接断开', '', '')
        netCable = eth2.isup
        # 是否进行网络认证
        if not eth2.isup:  # 此时没有插入网线
            lanNetStatus = False
            time.sleep(1)  # 检测时间为一秒
        if eth2.isup and lanNetStatus:  # 如果插入网线并且有网络连接
            time.sleep(5)
        if eth2.isup and lanNetStatus == False:  # 接入网线并且没有网络连接，也就是说要进行网络认证
            if connect(account, password, service):
                lanNetStatus = True


if __name__ == "__main__":
    main()
