from requests import post
import re
import datetime
import time

header = {
    "Host": "dfcz.upc.edu.cn",
    "Proxy-Connection": "keep-alive",
    "Content-Length": "3747",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "http://dfcz.upc.edu.cn",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "http://dfcz.upc.edu.cn/ShiYou/Default.aspx?code=uqioHvE4WDJrDXhnUAPreX5wDY9-mGrkjntmZOOW9eQ&state=STATE",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
roomNumber = []
for i in range(200, 900, 100):
    for j in range(1, 36):
        roomNumber.append(str(i + j))

sendKV = '__VIEWSTATE=%2FwEPDwUKMTkxNjAxNjUwMg9kFgICAw9kFghmDxAPFgYeDURhdGFUZXh0RmllbGQFB2xvdU5hbWUeDkRhdGFWYWx1ZUZpZWxkBQdsb3VOYW1lHgtfIURhdGFCb3VuZGdkEBUmCzAx5Y%2B35qW8KDEpCzAy5Y%2B35qW8KDIpCzAz5Y%2B35qW8KDMpCzA05Y%2B35qW8KDQpEjA05Y%2B35qW856m66LCDKDQ0KQswNeWPt%2BalvCg1KRIwNeWPt%2BalvOepuuiwgyg0NSkLMDblj7fmpbwoNikSMDblj7fmpbznqbrosIMoNDYpCzA35Y%2B35qW8KDcpEjA35Y%2B35qW856m66LCDKDQ3KQswOOWPt%2BalvCg4KRIwOOWPt%2BalvOepuuiwgyg0OCkSMDnlj7fmpbznqbrosIMoNDkpDDEw5Y%2B35qW8KDEwKRIxMOWPt%2BalvOepuuiwgyg1MCkMMTHlj7fmpbwoMTEpEjEx5Y%2B35qW856m66LCDKDUxKQwxMuWPt%2BalvCgxMikSMTLlj7fmpbznqbrosIMoNTIpDDEz5Y%2B35qW8KDEzKRIxM%2BWPt%2BalvOepuuiwgyg1MykMMTTlj7fmpbwoMTQpEjE05Y%2B35qW856m66LCDKDU0KQwxNeWPt%2BalvCgxNSkSMTXlj7fmpbznqbrosIMoNTUpDDE25Y%2B35qW8KDE2KRIxNuWPt%2BalvOepuuiwgyg1NikMMTflj7fmpbwoMTcpEjE35Y%2B35qW856m66LCDKDU3KQwxOOWPt%2BalvCgyMCkSMTjlj7fmpbznqbrosIMoNTgpDDE55Y%2B35qW8KDIxKRIxOeWPt%2BalvOepuuiwgyg1OSkQ55WZ5a2m55Sf5qW8KDIzKRTnoJTnqbbnlJ8x5Y%2B35qW8KDE5KRTnoJTnqbbnlJ8y5Y%2B35qW8KDE4KRTnoJTnqbbnlJ8z5Y%2B35qW8KDIyKRUmCzAx5Y%2B35qW8KDEpCzAy5Y%2B35qW8KDIpCzAz5Y%2B35qW8KDMpCzA05Y%2B35qW8KDQpEjA05Y%2B35qW856m66LCDKDQ0KQswNeWPt%2BalvCg1KRIwNeWPt%2BalvOepuuiwgyg0NSkLMDblj7fmpbwoNikSMDblj7fmpbznqbrosIMoNDYpCzA35Y%2B35qW8KDcpEjA35Y%2B35qW856m66LCDKDQ3KQswOOWPt%2BalvCg4KRIwOOWPt%2BalvOepuuiwgyg0OCkSMDnlj7fmpbznqbrosIMoNDkpDDEw5Y%2B35qW8KDEwKRIxMOWPt%2BalvOepuuiwgyg1MCkMMTHlj7fmpbwoMTEpEjEx5Y%2B35qW856m66LCDKDUxKQwxMuWPt%2BalvCgxMikSMTLlj7fmpbznqbrosIMoNTIpDDEz5Y%2B35qW8KDEzKRIxM%2BWPt%2BalvOepuuiwgyg1MykMMTTlj7fmpbwoMTQpEjE05Y%2B35qW856m66LCDKDU0KQwxNeWPt%2BalvCgxNSkSMTXlj7fmpbznqbrosIMoNTUpDDE25Y%2B35qW8KDE2KRIxNuWPt%2BalvOepuuiwgyg1NikMMTflj7fmpbwoMTcpEjE35Y%2B35qW856m66LCDKDU3KQwxOOWPt%2BalvCgyMCkSMTjlj7fmpbznqbrosIMoNTgpDDE55Y%2B35qW8KDIxKRIxOeWPt%2BalvOepuuiwgyg1OSkQ55WZ5a2m55Sf5qW8KDIzKRTnoJTnqbbnlJ8x5Y%2B35qW8KDE5KRTnoJTnqbbnlJ8y5Y%2B35qW8KDE4KRTnoJTnqbbnlJ8z5Y%2B35qW8KDIyKRQrAyZnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAgQPPCsACwEADxYIHghEYXRhS2V5cxYAHgtfIUl0ZW1Db3VudAIBHglQYWdlQ291bnQCAR4VXyFEYXRhU291cmNlSXRlbUNvdW50AgFkFgJmD2QWAgIBD2QWBgIBDw8WAh4EVGV4dAUIODEuNjTluqZkZAICDw8WAh8HBQowMDAxMDgwMDE5ZGQCAw8PFgIfBwUDODMzZGQCBQ88KwARAgEQFgAWABYADBQrAABkAgYPPCsAEQMADxYEHwJnHwQCAWQBEBYAFgAWAAwUKwAAFgJmD2QWBgIBD2QWCGYPDxYCHwcFCjAwMDEwODAwMTlkZAIBDw8WAh8HBQwxOOWPt%2BalvCgyMClkZAICDw8WAh8HBQM4MzNkZAIDD2QWAgIBDw8WAh4PQ29tbWFuZEFyZ3VtZW50BQ84MzMoMDAwMTA4MDAxOSlkZAICDw8WAh4HVmlzaWJsZWhkZAIDDw8WAh8JaGRkGAIFDnlvbmdodUdyaWRWaWV3DzwrAAwDBhUBCFlvbmdIdUlEBxQrAAEUKwABBQowMDAxMDgwMDE5CAIBZAUNeW9uZ2h1R291RGlhbg9nZA3D%2BV%2BvgqnmB3XkLgJrDVksAcTO7Ck%2F45w4NBk78c96&__VIEWSTATEGENERATOR=2A6178C9&__EVENTVALIDATION=%2FwEdACtWIA18IwlkoRg7gOKYsNTuciSO0eblAjNiOyMJvhERh8g0cLcy1HkEyE%2F%2Fo8NpI68Tqo4PWi9WlAxvOPs3Z8FlttYAwjuUDFOpDcny3bbvrFytnZTIO1G1vq2mP3Fqsql3Eqv0lDmQ%2BMqRBjifloFc3dyYduLlYtMgano67Cf2EGm17suCjg%2FcP5zBe%2B0weN64dClm40YrasFTHgpXJJ%2F24817XGZOKxTOHeGtOrc69y10NEXTK3nXSGBfpA%2Fe3cb8SXL4ozPg%2FH0y%2FXJe6aAjjl9XWtSdw%2B3wgoxhRCiyPkynoZYHMfkQCXuPetkRJaacsV205eWAERkqSBBYDNb%2BP%2FSIx77oMlUbhVrxpziiv3eWVd4KyL6VAwsGlUPx9FjBfgVTM7l4amSGInVrH5u%2FqNvQmxm%2F8ml%2F6XH6inhTIQZyzoRUf1YIo2Ol6h9DEEghH8WHUklvPqoc6BroTiyzaeJ%2BLoXYOEFcT%2FZkCWmhKOQiQbzQ%2FuEKT%2FXZUv8LIuOAWRxUeUgP08yY4qH9eN2J%2FsXTUD%2BiV18Q82wX5hBOOKCtQ577tb%2FJ%2FI30OxTZZSPzR0Tsh5zwHPcsHrMhTKI9R4XKOPLU9Wbc1ivlWDdRA7qsizF0GfRfSzM5%2F71%2BnQHbOgdacv01mTxP%2F6gIpPkX3KlVo6TwjlGcWdhJmnJGJOY0ynznctoZRpwFkrTLRInGL%2BVj1dyh3Q9m%2Bs2vSeFrgkNdcExn7IGpFPksmdNkiTwheCssQ3PBd3Le%2BBvgeiHmRryKhyH1el%2FPylJrnw%2Bwbpli97Gqb0G15TiMvdE2GmrAkdIWwfN3Eo1%2BS6FgiOCfD0%2FrXOhPRRbmg5CvVw4F379khLm46wtCyYCo46y34P8k%2B2zVpk7P54SBBD56pkCHbyknVdszY%2BfFgKMx8o6v%2BIzOigzyJCPuKgxaDvfS3YnI7EjbxPF3Pq%2FnpYg0LH0%3D' \
         '&lou=18%E5%8F%B7%E6%A5%BC%2820%29' \
         '&yonghu={}&chaxun=%E6%9F%A5%E8%AF%A2'

rule = r'<td>(.*?)度</td>'


def getEle(KEY):
    data = post(
        'http://dfcz.upc.edu.cn/ShiYou/Default.aspx?code=uqioHvE4WDJrDXhnUAPreX5wDY9-mGrkjntmZOOW9eQ&state=STATE',
        headers=header, data=KEY)
    text = data.text
    ele = re.findall(rule, text)[0]
    return ele


def writeLine(name, value):
    f = open(name, 'a')
    f.write(value)
    f.close()

time.sleep(200)
while True:
    for name in roomNumber:
        try:
            filename = 'D:\data\\18号楼用电情况\\' + name + '.txt'
            e = getEle(sendKV.format(name))
            concurrentTime = datetime.datetime.now()
            res = str(concurrentTime) + "---" + e + '\n'
            # print(name + '--' + res)
            writeLine(filename, res)
            time.sleep(10)
        except:
            temp = 1
    time.sleep(10800)
