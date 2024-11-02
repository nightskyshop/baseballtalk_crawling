from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


# Hit, Homerun

driver.get("https://www.koreabaseball.com/Record/Player/HitterBasic/BasicOld.aspx")

kbo_select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
kbo_select.select_by_value("0")
time.sleep(1)

hit_btn = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > thead > tr > th:nth-child(9) > a")
hit_btn.click()
time.sleep(.5)
hit_third = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child(3) > td.asc").text
print(hit_third)

homerun_btn = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > thead > tr > th:nth-child(12) > a")
homerun_btn.click()
time.sleep(.5)
homerun_third = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child(3) > td.asc").text
print(homerun_third)

rbi_btn = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > thead > tr > th:nth-child(14) > a")
rbi_btn.click()
time.sleep(.5)
rbi_third = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child(3) > td.asc").text
print(rbi_third)

# Stolen Base

driver.get("https://www.koreabaseball.com/Record/Player/Runner/Basic.aspx")

stolenBase_third = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child(3) > td.asc").text


# Win, Inning

driver.get("https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx")

kbo_select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
kbo_select.select_by_value("0")
time.sleep(1)

win_btn = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > thead > tr > th:nth-child(6) > a")
win_btn.click()
time.sleep(.5)
win_second = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child(2) > td.asc").text

inning_btn = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > thead > tr > th:nth-child(11) > a")
inning_btn.click()
time.sleep(.5)
inning_third = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child(3) > td.asc").text


if "/" not in inning_third:
    inning = inning_third
else:
    innings = inning_third.split()

    inning_num = 0

    if len(innings) != 1:
        inning_num += float(int(innings[1].split("/")[0]) / 10)
    
    inning_num += float(innings[0])
    inning = inning_num


print(hit_third, homerun_third, rbi_third, stolenBase_third, win_second, inning)

data = {
    "maxHit": hit_third,
    "maxHomerun" : homerun_third,
    "maxRbi": rbi_third,
    "maxStolenBase": stolenBase_third,
    "maxWin": win_second,
    "maxInning": inning
}

requests.post("http://localhost:8080/maxData", json=data)
