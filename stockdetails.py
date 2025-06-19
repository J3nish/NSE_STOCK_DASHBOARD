import time
from datetime import datetime
from dbase import c, conn  # Database cursor and connection
from selenium import webdriver
from selenium.webdriver.common.by import By
import stockindia.constants as const
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class StockIndia(webdriver.Chrome):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'normal'
        super().__init__(options=options)
        self.implicitly_wait(10)
        self.maximize_window()

    def go_topage(self):
        self.get(const.BASIC_URL)

    def scrape_table(self):
        WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@id='equityStockTable']/tbody"))
        )

        rows = self.find_elements(By.XPATH, "//table[@id='equityStockTable']//tbody/tr")[1:31]

        # Clear old records (DO THIS ONLY ONCE)
        c.execute("DELETE FROM stocks")
        conn.commit()

        today = datetime.now().strftime('%Y-%m-%d')

        for i, row in enumerate(rows):
            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) < 10:
                print(f"Skipping row {i + 1}, not enough columns: {len(cols)}")
                continue

            company_name = cols[0].text
            open_price = float(cols[1].text.replace(',', ''))
            close_price = float(cols[4].text.replace(',', ''))
            ltp = float(cols[5].text.replace(',', ''))
            change = float(cols[8].text.replace(',', ''))
            volume = int(cols[9].text.replace(',', ''))

            # Insert into history table
            c.execute('''
                INSERT INTO stocks_history (date, company_name, open_price, close_price, ltp, change, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (today, company_name, open_price, close_price, ltp, change, volume))

            # Insert into daily table
            c.execute('''
                INSERT INTO stocks (company_name, open_price, close_price, ltp, change, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (company_name, open_price, close_price, ltp, change, volume))

        conn.commit()

if __name__ == "__main__":
    bot = StockIndia()
    bot.go_topage()
    time.sleep(5)
    bot.scrape_table()
    bot.quit()
    conn.close()
