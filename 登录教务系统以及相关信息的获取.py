import requests
import execjs
from lxml import etree
import json
from bs4 import BeautifulSoup
import re


def getRsa(u, p, lt):
    """
    加密方法
    :param u:账号
    :param p:密码
    :param lt:lt
    :return:加密值
    """
    jsPath = r'./des.js'
    with open(jsPath, "r") as file:
        desJsCode = file.read()
    desJsFunction = execjs.compile(desJsCode)
    rsa = desJsFunction.call("strEnc", u + p + lt, "1", "2", "3")
    return rsa


class USER:
    jwxt = False  # 教务系统
    rmfw = False  # 微信热门服务
    jwxtCookie = ""
    rmfwCookie = ""

    def __init__(self, account: str, password: str) -> None:
        """
        :param account: 数字石大账号
        :param password: 密码
        """
        self.account = account
        self.password = password

    def loginJWXT(self) -> bool:
        """
        登录教务系统
        :return:
        """
        """
        ----------------------------------------------------------------------------------
        第一次请求获取lt和execution的数值
        """
        header = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            # "Cache-Control": "max-age=0",
            # "Cookie": "Language=zh_CN; JSESSIONID=t2q85E9_6w98gizTgfyhchNFrQn2xZb7FfA0MY5ZYOwKCQHsrzIG!-1603879557",
            # "Host": "cas.upc.edu.cn",
            # "Proxy-Connection": "keep-alive",
            # "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
        }
        loginUrl = """http://cas.upc.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.upc.edu.cn%2Fneusoftcas.jsp"""
        session = requests.session()
        one = session.get(loginUrl, headers=header)
        loginPageHtml = etree.HTML(one.text)

        lt = loginPageHtml.xpath(r'//*[@id="lt"]/@value')[0]
        execution = loginPageHtml.xpath(r'//*[@name="execution"]/@value')[0]
        _eventId = "submit"
        ul = len(self.account)
        pl = len(self.password)
        rsa = getRsa(self.account, self.password, lt)
        """
        ----------------------------------------------------------------------------------
        第二次请求提交相应信息
        """
        data = {"rsa": rsa,
                "ul": ul,
                "pl": pl,
                "lt": lt,
                "execution": execution,
                "_eventId": _eventId
                }

        two = session.post(loginUrl, headers=header, data=data, allow_redirects=False)
        # nextUrl = re.findall("""<a href="(.*?)">""", r.text)[0]
        nextUrl = two.headers['Location']
        """
        ----------------------------------------------------------------------------------
        第三次请求进行对应跳转，获取教务系统相关cookie
        """
        header = {
            "Host": "jwxt.upc.edu.cn",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "http://cas.upc.edu.cn/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "close"
        }
        three = requests.get(nextUrl, headers=header, allow_redirects=False)
        cookie = three.headers['Set-Cookie']
        print('教务系统cookie：', cookie)
        """
        ----------------------------------------------------------------------------------
        第四次请求
        """
        header = {
            "Host": "jwxt.upc.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "http://jwxt.upc.edu.cn/neusoftcas.jsp;jsessionid=CE5776D8CDC09AAEE6177DBF430760C7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": cookie,
            "Connection": "close",
        }
        four = session.get("""http://jwxt.upc.edu.cn/Logon.do?method=logout""", headers=header, allow_redirects=False)
        fiveUrl = four.headers['Location']
        """
        ----------------------------------------------------------------------------------
        第五次请求
        """
        header = {
            "Host": "jwxt.upc.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "http://jwxt.upc.edu.cn/neusoftcas.jsp;jsessionid=CE5776D8CDC09AAEE6177DBF430760C7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": cookie,
            "Connection": "close",
        }
        five = session.get(fiveUrl, headers=header, allow_redirects=False)
        # print("cookie:\n", cookie)
        self.jwxtCookie = cookie
        self.jwxt = True
        return True

    def loginRMFW(self) -> bool:
        """
        登录热门服务
        :return:
        """
        temp = requests.session()

        loginHead = {
            'Host': 'app.upc.edu.cn',
            'Connection': 'keep-alive',
            'Content-Length': '44',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "X-Requested-With": 'X-Requested-With',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://app.upc.edu.cn',
            'Sec-Fetch-Site': 'Sec-Fetch-Site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://app.upc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.upc.edu.cn%2Fappsquare%2Fwap%2Fdefault%2Findex%3Fsid%3D4',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        data = {
            'username': self.account,
            'password': self.password
        }

        post1 = temp.post(url='https://app.upc.edu.cn/uc/wap/login/check', headers=loginHead, data=data)
        self.rmfwCookie = post1.headers['Set-Cookie']
        self.rmfw = True
        return True

    def timetable(self, year='2022-2023', term='2', week='15', tpe=2):
        """
        热门服务-课表
        :param res: 返回结果
        :param year: 学年 2022-2023
        :param term: 学期 2
        :param week: 周 15
        :param tpe: 返回类型 2
        :return:
        """
        if not self.rmfw or self.rmfwCookie == '':
            return []
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'eai-sess=fgdec63rsopq61hiat7vbah775; UUkey=085cd4a331e347a0cc5447e15d4bf011',
            'Host': 'app.upc.edu.cn',
            'Origin': 'https://app.upc.edu.cn',
            'Referer': 'https://app.upc.edu.cn/site/weekschedule/index',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        body = {
            'year': year,  # 年
            'term': term,  # 学期
            'week': week,  # 周
            'type': tpe  # 返回类型
        }
        data = requests.post(url="https://app.upc.edu.cn/timetable/wap/default/get-datatmp",
                             headers=header,
                             data=body)
        temp = json.loads(data.text)
        if temp['m'] != '操作成功':
            return []
        return temp

    def TheoreticalTimetable(self, year='2020-2021-1'):
        """
        教务系统-学期理论课表
        :param res: 返回结果
        :return:
        """
        if not self.jwxt or self.jwxtCookie == '':
            return []
        kbURL = """http://jwxt.upc.edu.cn/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL"""
        header = {
            "Host": "jwxt.upc.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "http://jwxt.upc.edu.cn/jsxsd/framework/xsMain.jsp",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": self.jwxtCookie,
            "Connection": "close"
        }
        data = {
            'cj0701id': '&zc=&demo=',
            'xnxq01id': year
        }
        html = requests.get(kbURL, headers=header, data=data).text
        # 解析
        soup = BeautifulSoup(html, 'html.parser')
        classes = soup.findAll('tr')[2:-1]  # 第一到第五大节
        res = []
        for i in classes:
            res.append(i.findAll('td'))
        # 对每个单元进行解析
        # res为5*7二维列表
        # 第一个空为第几大节课  0-第一大节  1-第二大节
        # 第二个空为第几周      0-周日     1-周一     6-周六
        # res[0][1] 表示 第一大节课 周一
        for i in range(len(res)):
            for j in range(len(res[0])):
                tempText = res[i][j].text.split('\n')
                tempList = []
                for line in tempText:
                    if line != '':
                        tempList.append(line)
                tempDict = {}
                line1 = tempList[0].split('----------------')
                line2 = tempList[1].split('---------------------')
                count = len(line1)
                for flag in range(count):
                    tempDict[line1[flag]] = line2[flag]
                res[i][j] = tempDict
        return res

    def grade(self, year='2022-2023-1'):
        """
        教务系统-成绩
        :param res: 返回结果
        :param year:
        :return:
        """
        gradeUrl = """http://jwxt.upc.edu.cn/jsxsd/kscj/cjcx_list"""
        header = {
            "Host": "jwxt.upc.edu.cn",
            "Content-Length": "37",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "http://jwxt.upc.edu.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.91 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Referer": "http://jwxt.upc.edu.cn/jsxsd/kscj/cjcx_query?Ves632DSdyV=NEW_XSD_XJCJ",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": self.jwxtCookie,
            "Connection": "close",
        }

        data = {
            'kksj': year,  # 选择学期
            'xsfs': 'all'
        }
        # 解析
        html = requests.post(gradeUrl, headers=header, data=data).text
        res = []
        res.append(html)
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.findAll('tr')
        # 表头处理
        result = []
        line = []
        for th in trs[1].findAll('th'):
            line.append(th.text)
        result.append(line)
        trs = trs[2:]
        for tr in trs:
            line = []
            tds = tr.findAll('td')
            for td in tds:
                line.append(td.text)
            result.append(line)
        return res


if __name__ == '__main__':
    user = USER('account', 'password')
    user.loginJWXT()
    user.loginRMFW()
    print(user.jwxtCookie)
    print(user.rmfwCookie)
    timeTabel = []
    flag1 = user.timetable(year='2022-2023', term='2', week='15')
    timeTabel1 = []
    flag2 = user.TheoreticalTimetable(year='2020-2021-2')
    grade = []
    flag3 = user.grade(year='2022-2023-1')
