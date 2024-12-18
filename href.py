import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

def setup_edge_driver():
    """
    Set up Microsoft Edge WebDriver.
    """
    edge_driver_path = r"Driver_Notes\msedgedriver.exe"  # Update with your actual path
    driver = webdriver.Edge(service=Service(edge_driver_path))
    return driver

def save_to_csv(filename, data, headers=None):
    """
    Save a list of data to a CSV file.
    """
    try:
        mode = 'a' if headers is None else 'w'
        with open(filename, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if headers:
                writer.writerow(headers)
            writer.writerows([[item] for item in data])
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

def scrape_links(driver, wait):
    """
    Scrape match links from divs with class 'result-con' and
    the next page link from an <a> with class 'pagination-next'.
    """
    match_links = []
    next_page_link = None

    try:
        # Scrape match links from divs with class 'result-con'
        print("Scraping match links...")
        result_divs = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.result-con"))
        )
        for div in result_divs:
            a_tag = div.find_element(By.TAG_NAME, "a")
            href = a_tag.get_attribute("href")
            if href:
                match_links.append(href)
        print(f"Found {len(match_links)} match links.")

        # Scrape the next page link from <a class="pagination-next">
        print("Scraping next page link...")
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, "a.pagination-next")
            next_page_link = next_page.get_attribute("href")
            print(f"Next page link: {next_page_link}")
        except Exception as e:
            print("No next page link found.")

    except Exception as e:
        print("Error while scraping links:")
        traceback.print_exc()

    return match_links, next_page_link

def scrape_and_save_links(url):
    """
    Main function to scrape match links and next page link and save them to CSV files.
    """
    driver = setup_edge_driver()
    try:
        # Open the target URL
        driver.get(url)
        wait = WebDriverWait(driver, 20)  # Adjust timeout as needed

        # Scrape links
        match_links, next_page_link = scrape_links(driver, wait)

        # Save match links to 'links_matches.csv'
        if match_links:
            save_to_csv('links_matches.csv', match_links, headers=["Match Links"])

        # Save the next page link to 'next_pages.csv'
        if next_page_link:
            save_to_csv('next_pages.csv', [next_page_link], headers=["Next Page Link"])

    except Exception as e:
        print("Error during scraping:")
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    # Example usage
    url = "https://www.hltv.org/results"
    scrape_and_save_links(url)
