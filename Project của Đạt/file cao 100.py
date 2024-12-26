import numpy as np
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

# Hàm khởi tạo trình duyệt mới
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Chạy trình duyệt ở chế độ không hiển thị
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

# Hàm cuộn trang
def scroll_page(driver, scroll_count=10, pause=1.5, offset=25):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = (total_height - offset) / scroll_count
    for i in range(1, scroll_count + 1):
        driver.execute_script(f"window.scrollTo(0, {i * scroll_step});")
        sleep(pause)

# Hàm thu thập tiêu đề và liên kết
def collect_titles_and_links(driver, limit=1000):
    collected_data = []
    collected_links = set()
    driver.get("https://vnexpress.net/goc-nhin")
    driver.maximize_window()

    while len(collected_links) < limit:
        articles = driver.find_elements(By.CSS_SELECTOR, "article.item-news")
        if not articles:
            scroll_page(driver, scroll_count=10)
            continue
        for article in articles:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, "h3.title-news a")
                title = title_element.text
                link = title_element.get_attribute("href")
                if link not in collected_links:
                    collected_links.add(link)
                    collected_data.append({"Title": title, "Link": link})
                    print(f"Collected: {len(collected_links)}/{limit} articles")
                    if len(collected_links) >= limit:
                        break
            except NoSuchElementException:
                continue
        scroll_page(driver, scroll_count=5)
    return collected_data

# Hàm thu thập thông tin chi tiết bài viết
def extract_detail_info(article):
    driver = init_driver()
    try:
        driver.get(article["Link"])
        sleep(2)
        date_element = driver.find_element(By.CSS_SELECTOR, "span.date")
        date = date_element.text
        title_detail_element = driver.find_element(By.CSS_SELECTOR, "h1.title-detail")
        detailed_title = title_detail_element.text
        description_element = driver.find_element(By.CSS_SELECTOR, "p.description")
        detailed_description = description_element.text
        content_paragraphs = driver.find_elements(By.CSS_SELECTOR, "article.fck_detail p")
        content = "\n".join([paragraph.text for paragraph in content_paragraphs])
        scroll_page(driver, scroll_count=10, pause=1.5, offset=50)
        return {
            "Date": date,
            "Detailed Title": detailed_title,
            "Author's Position": detailed_description,
            "Content": content,
            **article,
        }
    except NoSuchElementException:
        return {**article, "Error": "Failed to fetch details"}
    finally:
        driver.quit()

# Thu thập thông tin chi tiết từ danh sách bài viết với đa luồng
def collect_details_multithread(articles, max_workers=5):
    detailed_data = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(extract_detail_info, articles)
        for result in results:
            detailed_data.append(result)
    return detailed_data

# Chạy chương trình
if __name__ == "__main__":
    # Khởi tạo trình duyệt để thu thập liên kết
    driver = init_driver()
    articles = collect_titles_and_links(driver, limit=100)
    driver.quit()  # Đóng trình duyệt sau khi thu thập liên kết

    # Thu thập thông tin chi tiết với đa luồng
    detailed_articles = collect_details_multithread(articles, max_workers=5)

    # Lưu vào DataFrame và hiển thị
    df = pd.DataFrame(detailed_articles)
    print(df)

    # Lưu vào file Excel
    # Lưu vào file Excel
    df.to_excel("D:/du lieu o cu/HUTECH Courses/Social Networking Course/SocialNetworkingProject/Project của Đạt/vnexpress_articles_1.xlsx")
