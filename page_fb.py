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
        writer.writerow(["Post Text", "Reactions Count", "Comments Count"])

        try:
            driver.get("http://www.facebook.com/")  # Open Facebook

            time.sleep(2)

            phone_field = driver.find_element(By.ID, "email")
            password_field = driver.find_element(By.ID, "pass")

            phone_field.send_keys("0836320679")  
            password_field.send_keys("Voducduy") 

            password_field.send_keys(Keys.RETURN)  # Press Enter

            time.sleep(5)

            driver.get("https://www.facebook.com/mpclub26")  # Navigate to the specific page

            time.sleep(5)

            scroll_and_extract_posts(driver, writer)

        finally:
            driver.quit()

def scroll_and_extract_posts(driver, writer):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  

        extract_posts_text(driver, writer)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_posts_text(driver, writer):
    try:
        posts = driver.find_elements(By.XPATH, "//div[@data-ad-preview='message']")

        for index, post in enumerate(posts):
            post_xpath = f"(//div[@data-ad-preview='message'])[{index + 1}]"

            reaction_count_xpath = f"({post_xpath}/ancestor::*[3]/following-sibling::*[1]//div/following-sibling::*[1]/span/span)[1]"
            comment_count = f"(((//div[@data-ad-preview='message'])[{index+1}])/ancestor::*[3]/following-sibling::*[1]//div[@role='button'])[4]"
            print("fffff: ", comment_count)
            re = driver.find_element(By.XPATH, reaction_count_xpath)
            cm = driver.find_element(By.XPATH, comment_count)
            rec = re.text
            cmc = cm.text
            post_text = post.text
            if post_text.strip():
                print(post_text)
                print("=====")
                print(rec)
                print("=====")
                print(cmc)
            writer.writerow([post_text, rec, cmc])
            writer.writerow("")
        

    except Exception as e:
        print(f"Error extracting posts: {e}")



if __name__ == "__main__":
    main()
