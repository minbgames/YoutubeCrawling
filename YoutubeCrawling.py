from bs4 import BeautifulSoup

import time
from time import localtime, strftime

import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

webdriver_path = "/chromedriver_mac_arm64/chromedriver"
url = 'https://www.youtube.com/@minbgames/videos'

driver = webdriver.Chrome() # 따로 다운받지 않아도 됨 115 이후부터
driver.get(url)

# 스크롤 내리기
time.sleep(5)
endKey = 5
actions = driver.find_element(By.CSS_SELECTOR, 'body')
while endKey:
    actions.send_keys(Keys.END)
    time.sleep(0.3)
    endKey -= 1
print("Page Load Completed!")

# 데이터 수집 시작 확인
isStart = input("Start Code?")
while True:
    if isStart == "yes":
        break

# 데이터 수집 시작
print("Start Get Data....")

page = driver.page_source
soup = BeautifulSoup(page,'lxml')

all_title = soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer')
title = [soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer')[n].string for n in range(0,len(all_title))]

all_video_time = soup.find_all('span','style-scope ytd-thumbnail-overlay-time-status-renderer')
video_time = [soup.find_all('span','style-scope ytd-thumbnail-overlay-time-status-renderer')[n].string.strip() for n in range(0,len(all_video_time))]

#채널명
chennel = soup.find('yt-formatted-string',class_='style-scope ytd-channel-name').string
#구독자 수
sub_num = soup.find('yt-formatted-string',id='subscriber-count').string
#조회수, 올린지 얼마나 되었는지(업로드 시점)
c = soup.find_all('span','style-scope ytd-grid-video-renderer')
view_num = [soup.find_all('span','style-scope ytd-grid-video-renderer')[n].string for n in range(0,len(c))]

#현재 시간
extract_date = strftime("%Y/%m/%d %H:%M:%S", localtime())

youtube_video_list = []

x = 0		#조회수의 index
y = 1		#업로드 시점의 index

for i in range(0,len(all_title)-1):
    roww = []

    # roww.append(extract_date)
    # roww.append(chennel)
    # roww.append(sub_num)

    roww.append(title[i])
    roww.append(video_time[i].strip())
    roww.append(view_num[x])
    x += 2 #조회수만 append
    roww.append(view_num[y])
    y += 2 #업로드 시점만 append

    youtube_video_list.append(roww) #2차원 list

print("Export youtube Data...")
csvfile = open("youtubeData.csv","w",newline="")
csvwriter = csv.writer(csvfile)
for row in youtube_video_list:
    csvwriter.writerow(row)
csvfile.close()
print("Youtube Exported Data Completed!")