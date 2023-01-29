import time
import requests
from bs4 import BeautifulSoup as bs
import configparser
import os
import re
import json

class Auto:
    def __init__(self, info):
        self.courseList = []
        self.account = info[0]
        self.password = info[1]
        self.token = info[2]
        self.deptdb = ['300', '302', '303', '305', '309', '322', '323', '325', '329', '330', '352', '353', '355', '500', '505', '530', '531', '532', '554', '600', '601', '602', '603', '604', '608', '621', '622', '623', '624', '656', '700', '304', '701', '702',
                       '705', '721', '722', '723', '724', '725', '751', '754', '800', '310', '311', '312', '313', '331', '332', '333', '359', '360', '361', '301', '307', '308', '326', '327', '328', '356', '357', '358', 'A00', 'A21', '901', '903', '904', '906', '907']
        # for requests
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

        self.baseURL = "https://portalfun.yzu.edu.tw/cosSelect/"
        self.loginUrl = '{}login.aspx'.format(self.baseURL)
        self.captchaUrl = '{}ImageCode.aspx'.format(self.baseURL)
        self.indexURL = '{}index.aspx'.format(self.baseURL)

        self.loginPayLoad = {
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '',
            '__EVENTVALIDATION': '',
            'uid': self.account,
            'pwd': self.password,
            'Code': '',
            'Button1': '登入'
        }

    def login(self):
        while True:
            self.session.cookies.clear()
            with self.session.get(self.captchaUrl, stream=True, allow_redirects=False) as captchaHtml:
                captcha = captchaHtml.cookies['CheckCode']

            loginHtml = self.session.get(self.loginUrl)
            parser = bs(loginHtml.text, 'html.parser')
            self.loginPayLoad['__VIEWSTATE'] = parser.select("#__VIEWSTATE")[
                0]['value']
            self.loginPayLoad['__VIEWSTATEGENERATOR'] = parser.select(
                "#__VIEWSTATEGENERATOR")[0]['value']
            self.loginPayLoad['__EVENTVALIDATION'] = parser.select("#__EVENTVALIDATION")[
                0]['value']
            self.loginPayLoad['Code'] = captcha

            result = self.session.post(self.loginUrl, data=self.loginPayLoad)

            if ("parent.location='index.aspx'" in result.text):
                self.Consolelog('Login Successful! {}'.format(captcha))
                break
            else:
                self.Consolelog("Login Failed, Re-try!")

    def Consolelog(self, msg):
        temp = "{} {} ".format(time.strftime(
            "[%Y-%m-%d %H:%M:%S]", time.localtime()), msg)
        print(temp)
    #    self.LineNotifyLog(temp)

    def remove(self, item):
        if (item in self.courseList):
            self.courseList.remove(item)

    def exec(self):
        resDic = {}
        loading = 1
        for cd in self.deptdb:
            # courseId = ""
            courseDept = cd
            html = self.session.get(self.indexURL)
            if "login.aspx?Lang=TW" in html.text:
                self.login()

            # get info on the net
            html = self.session.get(self.indexURL)

            parser = bs(html.text, 'html.parser')
            PrePayLoad = {
                '__EVENTTARGET': 'DDL_Dept',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE':  parser.select("#__VIEWSTATE")[0]['value'],
                '__VIEWSTATEGENERATOR': parser.select("#__VIEWSTATEGENERATOR")[0]['value'],
                '__EVENTVALIDATION': parser.select("#__EVENTVALIDATION")[0]['value'],
                'Q': 'RadioButton1',
                'DDL_YM': parser.select('option')[0]['value'],
                'DDL_Dept': courseDept,
                'DDL_Degree': '1'
            }

            prePost = self.session.post(self.indexURL, data=PrePayLoad)
            parser = bs(prePost.text, 'html.parser')
            # print(prePost.text)

            PostPayLoad = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE':  parser.select("#__VIEWSTATE")[0]['value'],
                '__VIEWSTATEGENERATOR': parser.select("#__VIEWSTATEGENERATOR")[0]['value'],
                '__EVENTVALIDATION': parser.select("#__EVENTVALIDATION")[0]['value'],
                'Q': 'RadioButton1',
                'DDL_YM': '111,1  ',
                'DDL_Dept': courseDept,
                'DDL_Degree': '0',
                'Button1': '確定'
            }

            postPost = self.session.post(self.indexURL, data=PostPayLoad)
            result = bs(postPost.text, "html.parser")     # result of the request
            # print(postPost.text)
            resDic[courseDept] = self.getCourseInfo(result)
            print(f"loading: {loading}/{len(self.deptdb)} ~~")
            loading += 1
            # print(resDic)
        return resDic

    def getCourseInfo(self, soup):
        result = soup.select("#Table1")[0].select("tr")
        num = 0
        courseInfo = [[]]
        if soup.text.find("無課程資料") != -1:
            return [[]]
        for i in result:
            num += 1
            if (num % 2 == 1):
                continue
            else:
                tds = i.select("td")
                courseURL = self.baseURL + tds[1].select_one('a')['href'][2:]
                courseID = tds[1].select_one('a').text
                courseYear = tds[2].text
                courseName = tds[3].select_one('a').text
                isEnglish = True if tds[3].text.find("英語授課") != -1 else False
                courseType = tds[4].select_one('span').text
                child = tds[5].select_one('span').text.split()
                courseTime = []
                for j, s in enumerate(child):
                    if j==0 or j==len(child)-1:
                        courseTime.append(s)
                    else:
                        courseTime.append(s[1:len(s)-3])
                        courseTime.append(s[len(s)-3:len(s)])
                
                courseTeacher = tds[6].select_one('a').text if tds[6].select_one('a') else tds[6].text
                
                tempInfo = [courseURL, courseID, courseYear, courseName, isEnglish, courseType, courseTime, courseTeacher]
                # print(tempInfo)
                courseInfo.append(tempInfo)
        return courseInfo



if __name__ == "__main__":
    info = ['', '', '0']
    info[1] = os.environ["ACCESS_TOKEN"]
    info[0] = os.environ["ACCOUNT_TOKEN"]
    bot = Auto(info)
    bot.login()
    res = bot.exec()
    obj = json.dumps(res)
    # save
    with open("sample.json", "w") as outfile:
        outfile.write(obj)
