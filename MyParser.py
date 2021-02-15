import json
from db import create_session, Users
import requests
from bs4 import BeautifulSoup

http = 'http://85.26.146.169:80'
proxyDict = {"http": http}


def check_cookie(cookie):
    url = 'https://edu.tatar.ru/user/diary/week'
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://edu.tatar.ru',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://edu.tatar.ru/logon',
        'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
    }
    response = requests.request("GET", url, headers=headers, allow_redirects=True, proxies=proxyDict)
    try:
        a = response.history[1].url
        return True
    except:
        return False


def check_user(login, password):
    url = "https://edu.tatar.ru/logon"
    payload = f'main_login={login}&main_password={password}'
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://edu.tatar.ru',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://edu.tatar.ru/logon',
        'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxyDict)
    if 'err_text' in response.text:
        return False
    else:
        return response.cookies['DNSID']


def get_name(login, password):
    url = "https://edu.tatar.ru/logon"
    payload = f'main_login={login}&main_password={password}'
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://edu.tatar.ru',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://edu.tatar.ru/logon',
        'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, proxies=proxyDict)
    except:
        return 'error'
    if 'Неверный логин или пароль.' in response.text:
        return 'error'
    session = response.cookies['DNSID']
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://edu.tatar.ru',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://edu.tatar.ru/logon',
        'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
        'Cookie': f'DNSID={session}'
    }
    res2 = requests.request('GET', f"https://edu.tatar.ru/user/anketa", headers=headers, proxies=proxyDict)
    soup = BeautifulSoup(res2.text, 'lxml')
    list = soup.find_all('table')
    ans = []
    for i in list[0].find_all('tr'):
        temp = []
        for j in i.text.split('\n'):
            if j != "":
                temp.append(j.strip())
        if len(temp) == 1:
            temp.append('null')
        return temp[1]


def day_info(login, password, day, cookie):
    try:
        session = cookie
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://edu.tatar.ru',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://edu.tatar.ru/logon',
            'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
            'Cookie': f'DNSID={session}'
        }
        res2 = requests.request('GET', f"https://edu.tatar.ru/user/diary/day?for={day}", headers=headers,
                                proxies=proxyDict)
        if 'Расписание не найдено' in res2.text:
            return "нет"
        soup = BeautifulSoup(res2.text, 'lxml')
        list = soup.find_all('tr')
        ans = []
        for i in range(2, len(list)):
            temp = []
            for j in list[i].text.split("\n"):
                if j != '':
                    temp.append(j)
            if len(temp) > 1:
                ans.append(temp)
        json_ans = {}
        a = []
        for i in ans:
            s = {}
            try:
                s["lesson_time"] = i[0]
                s["lesson_name"] = i[1]
                s["homework"] = i[2]
            except:
                s["lesson_time"] = i[0]
                s["lesson_name"] = i[1]
                s["homework"] = ''
            marks = ''
            if len(i) > 3:
                for j in range(3, len(i)):
                    marks += i[j]
                    marks += " "
            s["marks"] = marks
            a.append(s)
        json_ans["lessons"] = a
        return json_ans
    except:
        url = "https://edu.tatar.ru/logon"
        payload = f'main_login={login}&main_password={password}'
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://edu.tatar.ru',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://edu.tatar.ru/logon',
            'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
        }
        response = requests.request("POST", url, headers=headers, data=payload, proxies=proxyDict)
        session = create_session()
        user = session.query(Users).filter(Users.login == login).first()
        session = response.cookies['DNSID']
        user.cookie = session
        session.add(user)
        session.commit()
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://edu.tatar.ru',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://edu.tatar.ru/logon',
            'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
            'Cookie': f'DNSID={session}'
        }
        res2 = requests.request('GET', f"https://edu.tatar.ru/user/diary/day?for={day}", headers=headers,
                                proxies=proxyDict)
        if 'Расписание не найдено' in res2.text:
            return "нет"
        soup = BeautifulSoup(res2.text, 'lxml')
        list = soup.find_all('tr')
        ans = []
        for i in range(2, len(list)):
            temp = []
            for j in list[i].text.split("\n"):
                if j != '':
                    temp.append(j)
            if len(temp) > 1:
                ans.append(temp)
        json_ans = {}
        a = []
        for i in ans:
            s = {}
            try:
                s["lesson_time"] = i[0]
                s["lesson_name"] = i[1]
                s["homework"] = i[2]
            except:
                s["lesson_time"] = i[0]
                s["lesson_name"] = i[1]
                s["homework"] = ''
            marks = ''
            if len(i) > 3:
                for j in range(3, len(i)):
                    marks += i[j]
                    marks += " "
            s["marks"] = marks
            a.append(s)
        json_ans["lessons"] = a
        return json_ans
