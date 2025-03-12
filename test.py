from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (remove for debugging)

options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

BASE_URL = "https://kclpure.kcl.ac.uk/portal/en/studentTheses/"

def get_theses_from_page(page_number):
    url = f"{BASE_URL}?page={page_number}"
    print(url)
    val = driver.get(url)
    print(val)
    time.sleep(3)  # Allow JavaScript to load

    theses = []
    
    # Locate all thesis list items
    results = driver.find_elements(By.CSS_SELECTOR, "li.list-result-item")
    print(results)


    for result in results:
        try:
            title_tag = result.find_element(By.CSS_SELECTOR, "h3.title a")
            author_tag = result.find_elements(By.CSS_SELECTOR, "a[rel='Person']")  # Gets multiple <a> tags (author + supervisor)
            date_tag = result.find_element(By.CSS_SELECTOR, "span.date")

            title = title_tag.text.strip()
            link = title_tag.get_attribute("href")
            author = author_tag[0].text.strip() if author_tag else "Unknown"  # First <a> should be the author
            date = date_tag.text.strip() if date_tag else "Unknown"

            theses.append({"Title": title, "Author": author, "Date": date, "Link": link})
        except Exception as e:
            print(f"Error extracting thesis: {e}")

    return theses

# Scrape multiple pages
all_theses = []
for page in range(0, 5):  # Adjust range as needed
    print(f"Scraping page {page}...")
    all_theses.extend(get_theses_from_page(page))

# Close the Selenium browser
driver.quit()

# Save to CSV
df = pd.DataFrame(all_theses)
df.to_csv("kcl_theses.csv", index=False)

print("Scraping complete. Data saved to kcl_theses.csv")
