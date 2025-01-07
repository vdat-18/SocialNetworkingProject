import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def main():
    chrome_driver_path = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    with open("facebook_posts_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Post Text", "Reactions Count", "Comments Count","Share Post","User"])

        try:
            driver.get("http://www.facebook.com/")  # Open Facebook

            time.sleep(2)

            phone_field = driver.find_element(By.ID, "email")
            password_field = driver.find_element(By.ID, "pass")

            phone_field.send_keys("0836320679")  
            password_field.send_keys("Voducduy")

            password_field.send_keys(Keys.RETURN)  # Press Enter

            time.sleep(5)

            driver.get("https://www.facebook.com/groups/416709328396092")  # Navigate to the specific page

            time.sleep(5)

            scroll_and_extract_posts(driver, writer, 4)

        finally:
            driver.quit()

def scroll_and_extract_posts(driver, writer, srcoll_time):
    last_height = driver.execute_script("return document.body.scrollHeight")/2

    for i in range(srcoll_time):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)  

        extract_posts_text(driver, writer)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_posts_text(driver, writer):
    try:
        #(//div[@role='feed']/div[2]//a)[3]
        posts = driver.find_elements(By.XPATH, "//div[@role='feed']")
        print("posts: ", posts)

        for index, post in enumerate(posts):
            #get post user
            #   
            user_xpath = f"(//div[@role='feed']/div[{index + 1}]//a)[3]"
            content_xpath = f"((//div[@role='feed']/div[{index +1}])//div[@dir='auto'])[2]"

            
            use = driver.find_element(By.XPATH, user_xpath)
            post = driver.find_element(By.XPATH, content_xpath)
            print("==========")
            print(index)
            print(use)
            print("======")
            print(post)

            writer.writerow("")



    except Exception as e:
        print(f"Error extracting posts: {e}")

if __name__ == "__main__":
    main()
