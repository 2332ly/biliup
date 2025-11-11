import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook

#配置区
vmid = "401315430"  # 改成UP主UID
output_path = r"D:\bili_videos.xlsx"  # 改成你的绝对路径
wait_login = True  # True：启动时手动登录
max_scroll = 3     # 最大爬取页数

#浏览器配置
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(), options=chrome_options)
driver.get(f"https://space.bilibili.com/{vmid}/video")

if wait_login:
    input(" 登录完成/不进行登录 按回车继续...")

wb = Workbook()
ws = wb.active
ws.append(["标题", "链接", "播放数", "弹幕数", "时长"])

#翻页循环
for page in range(1, max_scroll + 1):
    print(f"正在爬取第 {page} 页...")

    # 等待页面加载
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    #提取视频信息
    videos = driver.find_elements(By.CSS_SELECTOR, "div.bili-video-card")
    for v in videos:
        try:
            title_el = v.find_element(By.CSS_SELECTOR, ".bili-video-card__title a")
            title = title_el.text.strip()
            link = title_el.get_attribute("href").replace("//", "https://")

            stats = v.find_elements(By.CSS_SELECTOR, ".bili-cover-card__stat span")
            play = stats[0].text if len(stats) > 0 else ""
            danmu = stats[1].text if len(stats) > 1 else ""
            duration = stats[2].text if len(stats) > 2 else ""

            ws.append([title, link, play, danmu, duration])
        except Exception as e:
            print("跳过异常视频块：", e)

    #翻页控制
    try:
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'下一页')]")
        if "vui_button--disabled" in next_btn.get_attribute("class"):
            print("已到最后一页，停止。")
            break
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)
    except Exception as e:
        print("找不到下一页按钮或翻页失败：", e)
        break

print("爬取完成，正在保存...")

#保存到 Excel
wb.save(output_path)
print("已保存到：", output_path)
driver.quit()
