from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

url = "https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx"

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get(url)

kbo_select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
kbo_select.select_by_value("0")
time.sleep(1)

requests.post("https://baseballtalk.site/pitcher?flag=start", json={})

print("UNRAKED")
# Unranked Pitchers
for team in range(1, 11):
    try:
        select = Select(driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ddlTeam_ddlTeam'))
    except:
       print("err-25 select")
       continue

    time.sleep(.5)
    
    select.select_by_index(team)

    time.sleep(1)
    
    btns = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > div.paging > a")

    print(f"btns: {len(btns)}")
    for i in range(1 if len(btns) > 1 else 0, len(btns)-1 if len(btns) > 1 else 1):
        time.sleep(.1)
        try:
            btn = driver.find_element(By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_udpContent > div.record_result > div.paging > a:nth-child({i+1})")
            btn.click()
        except:
           print(f"err-41 btn {i+1}")
           continue
        
        time.sleep(.5)

        trs = driver.find_elements(By.CSS_SELECTOR, "div.record_result > table.tData01 > tbody > tr")

        for i in range(1, len(trs) + 1):
            time.sleep(.5)

            try:
                data = {}
                tr = driver.find_element(By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child({i})")
            
                time.sleep(.1)

                index = tr.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
                name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2) > a")
                team = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
                era = tr.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
                game = tr.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
                win = tr.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
                lose = tr.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text
                save = tr.find_element(By.CSS_SELECTOR, "td:nth-child(8)").text
                hold = tr.find_element(By.CSS_SELECTOR, "td:nth-child(9)").text
                inning = tr.find_element(By.CSS_SELECTOR, "td:nth-child(11)").text
            except:
               print(f"err-68 data {team} {i}")
               continue

            if "-" in era or "-" in game or "-" in inning:
               continue

            data["rank"] = int(index)
            data["name"] = name.text

            if team == "LG": data["team"] = 2
            if team == "두산": data["team"] = 1
            if team == "한화": data["team"] = 3
            if team == "NC": data["team"] = 4
            if team == "KT": data["team"] = 5
            if team == "KIA": data["team"] = 6
            if team == "삼성": data["team"] = 7
            if team == "롯데": data["team"] = 8
            if team == "SSG": data["team"] = 9
            if team == "키움": data["team"] = 10

            data["era"] = float(era)
            data["game"] = int(game)
            data["win"] = int(win)
            data["lose"] = int(lose)
            data["save"] = int(save)
            data["hold"] = int(hold)


            
            if "/" not in inning:
                data["inning"] = float(inning)
            else:
                innings = inning.split()

                inning_num = 0

                if len(innings) != 1:
                    inning_num += float(int(innings[1].split("/")[0]) / 10)
                    inning_num += float(innings[0])
                elif "/" in innings[0]:
                    inning_num += float(int(innings[0].split("/")[0]) / 10)
                else:
                    inning_num += float(innings[0])
                
                data["inning"] = inning_num

            link = name.get_attribute("href")

            driver.execute_script(f"window.open('{link}');")

            driver.switch_to.window(driver.window_handles[-1])

            image, height, weight, slg, obp, ops = None, None, None, None, None, None

            try:
                image = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_imgProgile").get_attribute("src")
                height_weight = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
                height, weight = height_weight.split("/")
                whip = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(11)").text
            
                if image: data["image"] = image
                if height: data["height"] = int(height[:-2])
                if weight: data["weight"] = int(weight[:-2])
                if whip: data["whip"] = float(whip)
            except:
                print("err-132 data2")

                try: 
                    image = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_imgProgile").get_attribute("src")
                    height_weight = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
                    height, weight = height_weight.split("/")
                    whip = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(11)").text
                
                    if image: data["image"] = image
                    if height: data["height"] = int(height[:-2])
                    if weight: data["weight"] = int(weight[:-2])
                    if whip: data["whip"] = float(whip)
                except:
                    print("ERR")
                   

            data["ranked"] = False
            
            print(data)

            requests.post("https://baseballtalk.site/pitcher?flag=none", json=data)

            driver.close()
            driver.switch_to.window(driver.window_handles[-1])



#-------------------------------------------------------------------------------------------------------------------------------------------------


print("RANKED")
driver.get(url)

kbo_select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
kbo_select.select_by_value("0")
time.sleep(1)

btns = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > div.paging > a")

time.sleep(.5)
# Ranked Pitchers
for i in range(1 if len(btns) > 1 else 0, len(btns)-1 if len(btns) > 1 else 1):
  time.sleep(.1)
  try:
    print(i)
    btn = driver.find_element(By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_udpContent > div.record_result > div.paging > a:nth-child({i+1})")
    btn.click()
  except:
     print("err-174 btn")
  
  time.sleep(.1)

  trs = driver.find_elements(By.CSS_SELECTOR, "div.record_result > table.tData01 > tbody > tr")

  print("len: ", len(trs), trs[-1].text)

  for i in range(1, len(trs) + 1):
    time.sleep(.5)

    try:
        data = {}
        tr = driver.find_element(By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child({i})")

        time.sleep(.1)
        index = tr.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2) > a")
        team = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        era = tr.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
        game = tr.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
        win = tr.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
        lose = tr.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text
        save = tr.find_element(By.CSS_SELECTOR, "td:nth-child(8)").text
        hold = tr.find_element(By.CSS_SELECTOR, "td:nth-child(9)").text
        inning = tr.find_element(By.CSS_SELECTOR, "td:nth-child(11)").text
    except:
       print("err-203 data")

    data["name"] = name.text

    if team == "LG": data["team"] = 2
    if team == "두산": data["team"] = 1
    if team == "한화": data["team"] = 3
    if team == "NC": data["team"] = 4
    if team == "KT": data["team"] = 5
    if team == "KIA": data["team"] = 6
    if team == "삼성": data["team"] = 7
    if team == "롯데": data["team"] = 8
    if team == "SSG": data["team"] = 9
    if team == "키움": data["team"] = 10

    data["era"] = float(era)
    data["game"] = int(game)
    data["win"] = int(win)
    data["lose"] = int(lose)
    data["save"] = int(save)
    data["hold"] = int(hold)

    if "/" not in inning:
        data["inning"] = float(inning)
    else:
        innings = inning.split()

        inning_num = 0

        if len(innings) != 1:
            inning_num += float(int(innings[1].split("/")[0]) / 10)
        
        inning_num += float(innings[0])
        data["inning"] = inning_num

    link = name.get_attribute("href")

    driver.execute_script(f"window.open('{link}');")

    driver.switch_to.window(driver.window_handles[-1])
            
    time.sleep(.1)

    image, height, weight, slg, obp, ops = None, None, None, None, None, None

    try:
      image = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_imgProgile").get_attribute("src")
      height_weight = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
      height, weight = height_weight.split("/")
      whip = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(11)").text
    
      if image: data["image"] = image
      if height: data["height"] = int(height[:-2])
      if weight: data["weight"] = int(weight[:-2])
      if whip: data["whip"] = float(whip)
    except:
      print("err-260 data2")

      try:
        image = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_imgProgile").get_attribute("src")
        height_weight = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
        height, weight = height_weight.split("/")
        whip = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(11)").text
        
        if image: data["image"] = image
        if height: data["height"] = int(height[:-2])
        if weight: data["weight"] = int(weight[:-2])
        if whip: data["whip"] = float(whip)
      except:
         print("ERR")

    data["ranked"] = True

    print(data)

    requests.post("https://baseballtalk.site/pitcher?flag=none", json=data)

    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


requests.post("https://baseballtalk.site/pitcher?flag=end", json=data)

time.sleep(.1)

driver.close()
driver.quit()