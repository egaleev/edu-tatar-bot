import datetime
import json
import re

from db import create_session, Users, Lessons
import requests
from bs4 import BeautifulSoup

headers1 = {
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


def check_cookie(cookie):
    url = 'https://edu.tatar.ru/user/diary/week'
    headers = headers1
    response = requests.request("GET", url, headers=headers, allow_redirects=True)
    try:
        a = response.history[1].url
        return True
    except:
        return False


def period_info(cookie):
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
    res2 = requests.request('GET', f"https://edu.tatar.ru/user/diary/term", headers=headers)
    soup = BeautifulSoup(res2.text, 'lxml')
    list = soup.find('select')
    amount = len(str(list).split('\n')) - 1
    period_name = list.find('option', value=1).text.split()[-1]
    ans = {}
    ans['name'] = period_name
    ans['amount'] = amount
    return ans


def check_user(login, password):
    url = "https://edu.tatar.ru/login"
    payload = f'main_login={login}&main_password={password}'
    headers = headers1
    response = requests.request("POST", url, headers=headers, data=payload)
    if 'err_text' in response.text:
        return False
    else:
        return response.cookies['DNSID']


def update_cookie(login, password):
    url = "https://edu.tatar.ru/login"
    payload = f'main_login={login}&main_password={password}'
    headers = headers1
    response = requests.request("POST", url, headers=headers, data=payload)
    if 'err_text' in response.text:
        return False
    else:
        return response.cookies['DNSID']


def get_name(login, password):
    url = "https://edu.tatar.ru/logon"
    payload = f'main_login={login}&main_password={password}'
    headers = headers1
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
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
    res2 = requests.request('GET', f"https://edu.tatar.ru/user/anketa", headers=headers)
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


def table(login, password, cookie, period):
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
    res2 = requests.request('GET', f"https://edu.tatar.ru/user/diary/term?term={period}", headers=headers)
    if 'Пользователь не найден' in res2.text:
        session = create_session()
        user = session.query(Users).filter(Users.login == login).first()
        cookie = update_cookie(login, password)
        user.cookie = cookie
        session.add(user)
        session.commit()
        return table(login, password, user.cookie, period)
    soup = BeautifulSoup(res2.text, 'lxml')
    list = soup.find_all('table', class_="table term-marks")
    body = f"<html><head></head>\n<body>{list[0]}</body></html>"
    soup = BeautifulSoup(body, 'lxml')
    list = soup.find_all('tbody')
    html_marks = f"<html><head></head>\n<body>{list[0]}</body></html>"
    soup2 = BeautifulSoup(html_marks, 'lxml')
    new_list = soup2.find_all('tr')
    marks = []
    for i in new_list:
        soup = BeautifulSoup(f"<html><head></head>\n<body>{i}</body></html>", 'lxml')
        temp = soup.find_all('td')
        temp_marks = []
        for j in temp:
            j = j.text.strip()
            if j != "" and j != 'просмотр':
                temp_marks.append(j)
        lesson_name = temp_marks[0]
        if len(temp_marks) == 1:
            middle = ''
            final = ''
            marks = ''
        else:
            if '.' in temp_marks[-2]:
                middle = temp_marks[-2]
                final = temp_marks[-1]
                marks = temp_marks[1:-2]
            else:
                middle = temp_marks[-1]
                marks = temp_marks[1:-1]
                final = ''
        ans = {}
        ans["lesson_name"] = lesson_name
        ans["marks"] = marks
        ans["middle"] = middle
        ans['final'] = final
    if 1 == list[0]:
        pass
    else:
        url = "https://edu.tatar.ru/logon"
        payload = f'main_login={login}&main_password={password}'
        response = requests.request("POST", url, headers=headers1, data=payload)
        db_session = create_session()
        user = db_session.query(Users).filter(Users.login == login).first()
        session = response.cookies['DNSID']
        user.cookie = session
        db_session.add(user)
        db_session.commit()
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
        res2 = requests.request('GET', f"https://edu.tatar.ru/user/diary/term?term={period}", headers=headers)
        soup = BeautifulSoup(res2.text, 'lxml')
        list = soup.find_all('tr')
        marks = []
        for i in range(1, len(list) - 1):
            temp = []
            for j in list[i].text.split("\n"):
                if j != '' and j != 'просмотр':
                    temp.append(j.lstrip())
            ans = {}
            ans['lesson_name'] = temp[0]
            ans['marks'] = temp[1:]
            marks.append(ans)
        json_marks = {}
        json_marks["lessons"] = marks
        return json_marks


def day_info(login, password, day, cookie):
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
    res2 = requests.request('GET', f"https://edu.tatar.ru/user/diary/day?for={day}", headers=headers)
    if 'Расписание не найдено' in res2.text:
        return "нет"
    if 'Пользователь не найден' in res2.text:
        session = create_session()
        user = session.query(Users).filter(Users.login == login).first()
        cookie = update_cookie(login, password)
        user.cookie = cookie
        session.add(user)
        session.commit()
        return day_info(login, password, day, user.cookie)
    soup = BeautifulSoup(res2.text, 'lxml')
    list = soup.find_all('table', class_='main')
    body = f"<html><head></head>\n<body>{list[0]}</body></html>"
    soup = BeautifulSoup(body, 'lxml')
    list = soup.find_all('tbody')
    html_marks = f"<html><head></head>\n<body>{list[0]}</body></html>"
    soup2 = BeautifulSoup(html_marks, 'lxml')
    new_list = soup2.find_all('tr', attrs={'style': 'text-align: center;'})
    ans = []
    for i in range(len(new_list)):
        soup = BeautifulSoup(f"<html><head></head>\n<body>{new_list[i]}</body></html>", 'lxml')
        temp = soup.find_all('td')
        s = {}
        s["lesson_time"] = temp[0].text.strip()
        s["lesson_name"] = temp[1].text.strip()
        s["homework"] = temp[2].text.strip()
        soup = BeautifulSoup(f"<html><head></head>\n<body>{new_list[i]}</body></html>", 'lxml')
        marks = soup.find_all('table', class_="marks")
        if len(marks) == 0:
            s['marks'] = ""
        else:
            s['marks'] = marks[0].text.strip()
        ans.append(s)
    js_ans = {}
    js_ans['lessons'] = ans
    return js_ans


def empty_split(str):
    ans = []
    if str != 'null':
        for i in str:
            ans.append(i)
    return ans


def get_new():
    session = create_session()
    users = session.query(Users).all()
    ans = []
    period = '-1'
    for user in users:
        if user.period_name == 'полугодие':
            current_datetime = datetime.datetime.now()
            month = current_datetime.month
            day = current_datetime.day
            if (day >= 1 and month >= 9) and (day < 31 and month <= 12):
                period = '1'
            else:
                period = '2'
        elif user.period_name == 'четверть':
            current_datetime = datetime.datetime.now()
            month = current_datetime.month
            day = current_datetime.day
            if (day >= 1 and month >= 9) and (day < 31 and month <= 10):
                period = '1'
            elif (day >= 9 and month >= 11) and (day < 31 and month <= 12):
                period = '2'
            elif (day >= 11 and month >= 1) and (day < 27 and month <= 3):
                period = '3'
            else:
                period = '4'
        else:
            return []
        all_marks_now = table(user.login, user.password, user.cookie, period)
        all_marks_from_db = session.query(Lessons).filter(Lessons.owner_tg_id == user.tg_id).all()
        temp = []
        for i in range(len(all_marks_from_db)):
            lesson_from_db = all_marks_from_db[i]
            lesson_current = all_marks_now['lessons'][i]
            current_marks = lesson_current['marks']
            if len(lesson_current['marks']) == 0:
                lesson_current['final'] = ''
                lesson_current['middle'] = ''
                current_marks = []
            elif '.' in current_marks[-2]:
                lesson_current['final'] = current_marks[-1]
                lesson_current['middle'] = current_marks[-2]
                current_marks = current_marks[1:-2]
            else:
                lesson_current['middle'] = current_marks[-1]
                current_marks = current_marks[1:-1]
                lesson_current['final'] = ''
            marks_from_db = empty_split(lesson_from_db.marks)
            if current_marks != marks_from_db:
                if len(current_marks) > len(marks_from_db):
                    new_marks = []
                    new_counter = 0
                    if len(current_marks) != len(marks_from_db):
                        for old_counter in range(len(marks_from_db)):
                            if current_marks[new_counter] != marks_from_db[old_counter]:
                                new_marks.append(current_marks[new_counter])
                                new_counter += 1
                            new_counter += 1
                        if new_marks == []:
                            new_marks = current_marks[len(marks_from_db):len(current_marks)]
                    if len(new_marks) == 1:
                        temp.append(user.tg_id)
                        temp.append(
                            f"📰 Новая оценка по предмету *{lesson_from_db.lesson_name}*: ```{new_marks[0]}```\nТекущий средний балл ➡ {lesson_current['middle']}")
                    elif len(new_marks) > 1:
                        temp.append(user.tg_id)
                        temp.append(
                            f"📰 Новые оценки по предмету *{lesson_from_db.lesson_name}*: ```{', '.join(new_marks.split())}```\nТекущий средний балл ➡ {lesson_current['middle']}")
                else:
                    temp.append(user.tg_id)
                    temp.append(
                        f"📰 Изменения в оценках по предмету *{lesson_from_db.lesson_name}*\nТекущий средний балл ➡ {lesson_current['middle']}")
                lesson_from_db.marks = ''.join(current_marks)
                lesson_from_db.middle = lesson_current['middle']
                lesson_from_db.final = lesson_current['final']
                session.add(lesson_from_db)
                session.commit()
                ans.append(temp)
    return ans
