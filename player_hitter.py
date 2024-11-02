from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

url = "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx?sort=HRA_RT"

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get(url)

kbo_select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
kbo_select.select_by_value("0")
time.sleep(1)

requests.post("http://localhost:8080/hitter?flag=start", json={})

print("UNRAKED")
# Unranked Hitters
for team in range(1, 11):
    try:
        select = Select(driver.find_element(By.CSS_SELECTOR, '#cphContents_cphContents_cphContents_ddlTeam_ddlTeam'))
    except:
       print("err-25 select")
       continue

    time.sleep(.1)
    
    select.select_by_index(team)

    time.sleep(.1)

    btns = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > div.paging > a")

    for i in range(1 if len(btns) > 1 else 0, len(btns)-1 if len(btns) > 1 else 1):
        time.sleep(.1)
        try:
            btn = driver.find_element(By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_udpContent > div.record_result > div.paging > a:nth-child({i+1})")
            btn.click()
        except:
           print("err-41 btn")
           continue

        time.sleep(.1)

        trs = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr")

        for i in range(1, len(trs) + 1):
            time.sleep(.5)

            try:
                data = {}
                tr = driver.find_element(By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr:nth-child({i})")

                time.sleep(.1)

                index = tr.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
                name = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2) > a")
                team = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
                avg = tr.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
                game = tr.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
                h = tr.find_element(By.CSS_SELECTOR, "td:nth-child(9)").text
                second_hit = tr.find_element(By.CSS_SELECTOR, "td:nth-child(10)").text
                third_hit = tr.find_element(By.CSS_SELECTOR, "td:nth-child(11)").text
                hr = tr.find_element(By.CSS_SELECTOR, "td:nth-child(12)").text
                rbi = tr.find_element(By.CSS_SELECTOR, "td:nth-child(14)").text
            except:
               print(f"err-68 data {team} {i}")
               continue

            if "-" in avg:
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

            data["avg"] = int("".join(avg.split(".")))
            data["game"] = int(game)
            data["hit"] = int(h)
            data["secondHit"] = int(second_hit)
            data["thirdHit"] = int(third_hit)
            data["homeRun"] = int(hr)
            data["rbi"] = int(rbi)

            link = name.get_attribute("href")

            driver.execute_script(f"window.open('{link}');")

            driver.switch_to.window(driver.window_handles[-1])
            
            time.sleep(.1)

            image, height, weight, slg, obp, ops = None, None, None, None, None, None

            try:
                image = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_imgProgile").get_attribute("src")
                height_weight = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
                height, weight = height_weight.split("/")
                slg = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(6)").text
                obp = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(7)").text
                ops = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(11)").text
                stolen_base = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div.tbl-type02.mb10 > table > tbody > tr > td:nth-child(13)").text
                stolen_base_percent = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(9)").text
            

                if image: data["image"] = image
                if height: data["height"] = int(height[:-2])
                if weight: data["weight"] = int(weight[:-2])
                if slg: data["slg"] = int("".join(slg.split(".")))
                if obp: data["obp"] = int("".join(obp.split(".")))
                if ops: data["ops"] = int("".join(ops.split(".")))
                if stolen_base: data["stolenBase"] = int(stolen_base)
            except:
                print("err-124 data2")

                try:
                    image = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_imgProgile").get_attribute("src")
                    height_weight = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
                    height, weight = height_weight.split("/")
                    slg = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(6)").text
                    obp = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(7)").text
                    ops = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(11)").text
                    stolen_base = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div.tbl-type02.mb10 > table > tbody > tr > td:nth-child(13)").text
                    stolen_base_percent = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(9)").text
                    
                    if image: data["image"] = image
                    if height: data["height"] = int(height[:-2])
                    if weight: data["weight"] = int(weight[:-2])
                    if slg: data["slg"] = int("".join(slg.split(".")))
                    if obp: data["obp"] = int("".join(obp.split(".")))
                    if ops: data["ops"] = int("".join(ops.split(".")))
                    if stolen_base: data["stolenBase"] = int(stolen_base)
                except:
                    print("ERR")

            data["ranked"] = False

            print(data)

            requests.post("http://localhost:8080/hitter?flag=none", json=data)

            driver.close()
            driver.switch_to.window(driver.window_handles[-1])



#------------------------------------------------------------------------------------------------------------------------------------------------------


driver.get(url)

kbo_select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlSeries_ddlSeries"))
kbo_select.select_by_value("0")
time.sleep(1)

print("RANKED")

btns = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > div.paging > a")

time.sleep(.5)
# Ranked Hitters
for i in range(1 if len(btns) > 1 else 0, len(btns)-1 if len(btns) > 1 else 1):
  time.sleep(.1)
  try:
    print(i)
    btn = driver.find_element(By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_udpContent > div.record_result > div.paging > a:nth-child({i+1})")
    btn.click()
  except:
    print("err-173 btn")

  time.sleep(.1)

  trs = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody > tr")

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
        avg = tr.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
        game = tr.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
        h = tr.find_element(By.CSS_SELECTOR, "td:nth-child(9)").text
        second_hit = tr.find_element(By.CSS_SELECTOR, "td:nth-child(10)").text
        third_hit = tr.find_element(By.CSS_SELECTOR, "td:nth-child(11)").text
        hr = tr.find_element(By.CSS_SELECTOR, "td:nth-child(12)").text
        rbi = tr.find_element(By.CSS_SELECTOR, "td:nth-child(14)").text
    except :
       print("err-178 data")
       

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

    data["avg"] = int("".join(avg.split(".")))
    data["game"] = int(game)
    data["hit"] = int(h)
    data["secondHit"] = int(second_hit)
    data["thirdHit"] = int(third_hit)
    data["homeRun"] = int(hr)
    data["rbi"] = int(rbi)

    link = name.get_attribute("href")

    driver.execute_script(f"window.open('{link}');")

    driver.switch_to.window(driver.window_handles[-1])
            
    time.sleep(.1)

    image, height, weight, slg, obp, ops = None, None, None, None, None, None

    try:
      image = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_imgProgile").get_attribute("src")
      height_weight = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
      height, weight = height_weight.split("/")
      slg = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(6)").text
      obp = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(7)").text
      ops = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(11)").text
      stolen_base = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div.tbl-type02.mb10 > table > tbody > tr > td:nth-child(13)").text
      stolen_base_percent = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(9)").text
      
      if image: data["image"] = image
      if height: data["height"] = int(height[:-2])
      if weight: data["weight"] = int(weight[:-2])
      if slg: data["slg"] = int("".join(slg.split(".")))
      if obp: data["obp"] = int("".join(obp.split(".")))
      if ops: data["ops"] = int("".join(ops.split(".")))
      if stolen_base: data["stolenBase"] = int(stolen_base)
    except:
      print("err-253 data2")

      try:
        image = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_imgProgile").get_attribute("src")
        height_weight = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
        height, weight = height_weight.split("/")
        slg = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(6)").text
        obp = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(7)").text
        ops = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(11)").text
        stolen_base = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div.tbl-type02.mb10 > table > tbody > tr > td:nth-child(13)").text
        stolen_base_percent = driver.find_element(By.CSS_SELECTOR, "#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr > td:nth-child(9)").text
        
        if image: data["image"] = image
        if height: data["height"] = int(height[:-2])
        if weight: data["weight"] = int(weight[:-2])
        if slg: data["slg"] = int("".join(slg.split(".")))
        if obp: data["obp"] = int("".join(obp.split(".")))
        if ops: data["ops"] = int("".join(ops.split(".")))
        if stolen_base: data["stolenBase"] = int(stolen_base)
      except:
        print("ERR")
      

    data["ranked"] = True

    print(data)

    requests.post("http://localhost:8080/hitter?flag=none", json=data)

    driver.close()
    driver.switch_to.window(driver.window_handles[-1])



requests.post("http://localhost:8080/hitter?flag=end", json=data)

time.sleep(.1)

driver.close()
driver.quit()