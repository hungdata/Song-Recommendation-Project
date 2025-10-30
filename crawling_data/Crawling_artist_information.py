import csv
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By  

opts = Options()
browser = webdriver.Chrome(options= opts)
browser.get("https://kworb.net/spotify/country/global_weekly_totals.html")

rows =  browser.find_elements(By.XPATH, "/html/body/div/div[4]/table/tbody/tr")
with open("spotify.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["artist", "Wks", "T10", "Pk	(x?)", "PkStreams ▾	", "Total"])
    for r in rows[:20]:
        cells = [td.text for td in r.find_elements(By.CSS_SELECTOR,"td")]
        print(f'cell is Artist and title {cells}')
browser.quit()