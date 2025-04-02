from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import asyncio
from telegram import Bot

# Telegram ayarları
TELEGRAM_TOKEN = 'BURAYA_KENDİ_BOT_TOKENİNİ_YAPIŞTIR'
TELEGRAM_CHAT_ID = '@eceacar13'

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def check_appointment():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://ita-schengen.idata.com.tr/tr")

        print("CAPTCHA girmeni bekliyorum...")
        input("CAPTCHA'yı çözüp 'Randevu Al' dedikten sonra burada ENTER'a bas: ")

        WebDriverWait(driver, 30).until(EC.url_contains("appointment-form"))

        # Seçimleri yap
        Select(driver.find_element(By.ID, "MainContent_ddlIl")).select_by_visible_text("İstanbul")
        time.sleep(1)
        Select(driver.find_element(By.ID, "MainContent_ddlIlce")).select_by_visible_text("İstanbul Ofis - Altunizade")
        time.sleep(1)
        Select(driver.find_element(By.ID, "MainContent_ddlKategori")).select_by_visible_text("Turistik")
        time.sleep(1)
        Select(driver.find_element(By.ID, "MainContent_ddlAltKategori")).select_by_visible_text("STANDART")
        time.sleep(1)
        Select(driver.find_element(By.ID, "MainContent_ddlKisiSayisi")).select_by_visible_text("3")
        time.sleep(2)

        result = driver.find_element(By.ID, "MainContent_lblSonuc").text.strip()
        print("Sonuç:", result)

        if "uygun randevu bulunamamıştır" not in result.lower():
            asyncio.run(send_telegram_message("📅 RANDEVU BULUNDU! Hemen bak:\nhttps://ita-schengen.idata.com.tr/tr/appointment-form"))
        else:
            print("Randevu yok.")

    except Exception as e:
        print("Hata oluştu:", e)
        asyncio.run(send_telegram_message(f"❌ Bot hata verdi:\n{e}"))
    finally:
        driver.quit()

if __name__ == "__main__":
    check_appointment()
