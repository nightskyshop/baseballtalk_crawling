from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

url = "https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx"

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get(url)

trs = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > table > tbody > tr")

team_data = []

for tr in trs:
  data = []

  rank = tr.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
  team_name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
  game = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
  win = tr.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
  lose = tr.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
  tie = tr.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
  win_avg = tr.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text

  data.append(team_name)
  data.append(int(rank))
  data.append(int(game))
  data.append(int(win))
  data.append(int(lose))
  data.append(int(tie))
  data.append(int("".join(win_avg.split("."))))

  print(data)

  team_data.append(data)

url = "https://www.koreabaseball.com/Record/Team/Hitter/Basic1.aspx"

driver.get(url)

kbo_select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
kbo_select.select_by_value("0")
time.sleep(1)

trs = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr")

for tr in trs:
  team_name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
  avg = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text

  for team in team_data:
    if team[0] == team_name:
      team.append(int("".join(avg.split("."))))

pitcher_btn = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.tab-depth2 > ul > li:nth-child(2) > a")
pitcher_btn.click()

time.sleep(.5)

kbo_select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
kbo_select.select_by_value("0")
time.sleep(1)

trs = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr")

for tr in trs:
  team_name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
  era = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text

  for team in team_data:
    if team[0] == team_name:
      team.append(float(era))

time.sleep(.5)

print(team_data)

for team in team_data:
  teamname_en = "TEAM En NAME"
  if team[0] == "LG": teamname_en = "LG Twins"
  if team[0] == "두산": teamname_en = "Doosan Bears"
  if team[0] == "한화": teamname_en = "Hanwha Eagles"
  if team[0] == "NC": teamname_en = "NC Dinos"
  if team[0] == "KT": teamname_en = "KT Wiz"
  if team[0] == "KIA": teamname_en = "KIA Tigers"
  if team[0] == "삼성": teamname_en = "Samsung Lions"
  if team[0] == "롯데": teamname_en = "Lotte Giants"
  if team[0] == "SSG": teamname_en = "SSG Landers"
  if team[0] == "키움": teamname_en = "Kiwoom Heros"

  # http://ec2-3-39-232-92.ap-northeast-2.compute.amazonaws.com:8080/team
  # http://localhost:8080/team


  requests.post("http://localhost:8080/team", json={
    "teamname": team[0],
    "teamnameEn": teamname_en,
    "ranknum": team[1],
    "game": team[2],
    "win": team[3],
    "lose": team[4],
    "tie": team[5],
    "winavg": team[6],
    "avg": team[7],
    "era": team[8]
  })

driver.close()
driver.quit()