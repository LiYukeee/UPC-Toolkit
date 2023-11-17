import winreg
from time import sleep
from requests import post
from win11toast import toast
import time


def system_proxy(open_or_close, host='127.0.0.1', port=7890):
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

def windows11Note(title, msg, icon_path):
    image = {
        'src': "C:\\Users\\LiYuke\\OneDrive\\图片\\255.jpg",
        'placement': 'hero'
    }

    toast(title, msg, image=image, icon="D:/data/image/图标.png")


if __name__ == "__main__":
    # ---------0---------
    # 关闭系统代理
    # 在有代理情况下无法完成登录
    time.sleep(5)
    system_proxy(False)
    # ---------1---------
    # 登录信息
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Origin": "http://lan.upc.edu.cn",
        "Host": "lan.upc.edu.cn",
    }
    account = ' '  # 用户名
    password = ' '  # 密码
    serviceChoice = 'ctcc'  # 选择服务：cmcc(中国移动) ctcc(中国电信) cucc(中国联通)
    if serviceChoice == "ctcc":
        msg = '中国电信'
    elif serviceChoice == 'cmcc':
        msg = '中国移动'
    elif serviceChoice == 'cucc':
        msg = '中国联通'
    else:
        msg = '其他'
    data = """userId={}&password={}&service={}&queryString=wlanuserip%253D121.249.158.235%2526wlanacname%253D%2526nasip%253D172.22.242.21%2526wlanparameter%253D08-26-ae-33-e4-70%2526url%253Dhttp%253A%252F%252Fwww.google.com%252F%2526userlocation%253Dethtrunk%252F62%253A1667.27&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false"""
    data = data.format(account, password, serviceChoice)
    res = ''
    i = 0
    tryTimes = 1
    icoPath = r"D:/data/image/图标.png"
    # ---------2---------
    # 登录
    for i in range(tryTimes):
        try:
            re = post('http://lan.upc.edu.cn/eportal/InterFace.do?method=login',
                      headers=header, data=data, proxies=None)
            res = re.text
            if 'success' in res:
                print("登录成功")
                windows11Note('网络认证成功', msg+"网络已连接", icoPath)
                break
        except:
            a = 1
        print("登录第{}次失败".format(i + 1))
        sleep(1)

    if i == tryTimes - 1:
        print("登录失败")
        windows11Note('登录网络失败', " ", icoPath)
    print("程序运行结束")
    # system_proxy(True)
