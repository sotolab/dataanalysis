# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from urllib.request import Request, urlopen
from time import sleep
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
import datetime
import traceback

import numpy as np

import openpyxl

import configparser

# reallink = []

def getList():
    reallink = []
    while True:
        pageString = driver.page_source
        bsObj = BeautifulSoup(pageString, "lxml")

        for link1 in bsObj.find_all(name="div",attrs={"class":"Nnq7C weEfm"}):
            # print("len link1:", len(link1.select('a')))
            for idx in range(len(link1.select('a'))):
                title = link1.select('a')[idx]
                real = title.attrs['href']
                reallink.append(real)


        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            else:
                last_height = new_height
                continue



    myset = set(reallink)
    reallink = list(myset)
    ilink = np.array(reallink)
    np.save("link"+name, ilink)
    print('### 저장완료 ', name)


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('config.ini')

    username = config['DEFAULT']['USERID']
    userpw = config['DEFAULT']['PASSWD']

    MAC = 0
    driver = ""

    wb = openpyxl.Workbook()
    sheet = wb.active
    
    name = "축구"  #input("검색어를 입력하세요 : " )
    print('### 검색어 ', name)

    if (MAC):
        # driver load
        driver = webdriver.Chrome(executable_path='./chromedriver')
    else:
        driver = webdriver.Chrome('chromedriver.exe')

    driver.set_window_size(600,600)

    loginUrl = 'https://www.instagram.com/accounts/login/'
    driver.implicitly_wait(5)

    # 웹 사이트 접속
    driver.get(loginUrl)

    # 사전 정보 정의

    #login
    login_id = driver.find_element_by_name('username')
    login_id.send_keys(username)
    login_pw = driver.find_element_by_name('password')
    login_pw.send_keys(userpw)
    login_pw.send_keys(Keys.RETURN)
    time.sleep(5)

    popup = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
    popup.send_keys(Keys.ENTER)
    time.sleep(3)
    popup = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
    popup.send_keys(Keys.ENTER)

    scrolltime = 1.5 

    search = urllib.parse.quote(name)
    url = 'https://www.instagram.com/explore/tags/'+str(search)+'/'
    # driver = webdriver.Chrome('chromedriver.exe')

    driver.get(url)
    sleep(5)

    now = datetime.datetime.now()
    SCROLL_PAUSE_TIME = 2.0

    reallink = []
    getList()

    reallink = np.load('link'+name+'.npy')
    hashtags2 = []
    totalLikes = 0

    reallinknum = len(reallink)
    print("총"+str(reallinknum)+"개의 데이터.")
    sheet.append([str(reallinknum)])

    try:  # 반복문 시작 ( print 명령어로 원하는 문자열인지 하나씩 확인해보시길 바랍니다.
        for i in range(0,reallinknum):
            hashtags2.append([])
            percen = ( i / reallinknum * 100)
            print(" count: (%d  @/ %d)" % (percen, i))
            driver.implicitly_wait(1)
            req = 'https://www.instagram.com/'+reallink[i]
            driver.get(req)
            # print("Links: ", req)
            webpage = driver.page_source
            soup = BeautifulSoup(webpage, "html.parser")
            #print(soup)
            # day = str(soup.find_all(name="time",attrs={"class":"_1o9PC Nzb55"}))
            # date = day.split('일">')[1].split('</time>')[0]
            # # print("date:", date)

            soup1 = str(soup.find_all(attrs={'class': 'e1e1d'}))
            #print(soup1)
            user_id = soup1.split('href="/')[1].split('/"')[0]
            #print(user_id)
            soup1 = str(soup.find_all(attrs={'class': 'Nm9Fw'}))
            #print(soup1)
            subValue = 'span'
            if(soup1=="[]"): #좋아요가 0개, 1개, n개 일경우 모두 소스가 다르다.
                likes = '0'
            elif( soup1.find(subValue)==-1):
                likes = '0' #soup1.split('좋아요 ')[1].split('개')[0]
            elif( soup1.find(subValue)!=-1):
                likes = soup1.split('<span>')[1].split('</span>')[0]

            # totalLikes += int(likes)

            insert_data = {
                # "date" :  date,
                "likes" :  likes
            }
            # pandas_csv.to_csv(insert_data)

            soup1 = str(soup.find_all(attrs={'class': 'xil3i'}))
            if(soup1=="[]"): #해쉬태그가 없을 경우 소스가 다르다.
                hashtags = '해쉬태그없음'
                insert_data = {
                                "user_id" : user_id,
                                "좋아요" : likes}
                # pan_csv.to_csv(insert_data)
                # print("해쉬태그없음: ", insert_data)
            else:
                soup2 = soup1.split(',')
                soup2num = len(soup2)
                for j in range(0,soup2num):
                    hashtags = soup2[j].split('#')[1].split('</a>')[0]
                    # print("hashtags: ", hashtags)
                    insert_data = { "hashtags" : hashtags }
                    # print("저장성공: %s", insert_data)
                    sheet.append([hashtags])

    except Exception as error:
        print("오류발생: " + str(error))
        print(traceback.format_exc())

    nowDatetime = now.strftime('%Y-%m-%d-%H-%M-%S')
    wb.save(name + nowDatetime + ".xlsx")
    print("All 저장성공")
    # driver.quit()
