import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import traceback

def setup_edge_driver():
    """
    Set up Microsoft Edge WebDriver.
    """
    edge_driver_path = r"Driver_Notes\msedgedriver.exe"  # Update with your actual path
    driver = webdriver.Edge(service=Service(edge_driver_path))
    return driver

def file_exists(filename):
    """
    Check if the file exists.
    """
    return os.path.isfile(filename)

def save_to_csv(filename, data, headers=None):
    """
    Save a list of data to a CSV file, appending new entries without overwriting existing data.
    """
    try:
        # Open the file in append mode if it exists, otherwise in write mode
        mode = 'a' if file_exists(filename) else 'w'
        with open(filename, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write headers only if the file is new
            if headers and mode == 'w':
                writer.writerow(headers)
            writer.writerows([[item] for item in data])
            writer.writerow('\n')
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

def scrape_links_and_next_page(url):
    """
    Scrape match links from a given URL and save the results into two CSV files:
    - links_matches.csv for match links
    - next_pages.csv for the next page link
    """
    driver = setup_edge_driver()
    try:
        # Open the target URL
        driver.get(url)
        wait = WebDriverWait(driver, 20)  # Adjust timeout as needed

        # Scrape match links
        print("Scraping match links...")
        match_links = []
        result_divs = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.result-con"))
        )
        for div in result_divs:
            a_tag = div.find_element(By.TAG_NAME, "a")
            href = a_tag.get_attribute("href")
            if href:
                match_links.append(href)
        print(f"Found {len(match_links)} match links.")

        # Save match links to 'links_matches.csv'
        if match_links:
            save_to_csv('links_matches.csv', match_links, headers=["Match Links"])

        # Scrape next page link
        print("Scraping next page link...")
        next_page_link = None
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, "a.pagination-next")
            next_page_link = next_page.get_attribute("href")
            print(f"Next page link: {next_page_link}")
        except Exception as e:
            print("No next page link found.")

        # Save the next page link to 'next_pages.csv'
        if next_page_link:
            save_to_csv('next_pages.csv', [next_page_link], headers=["Next Page Link"])

    except Exception as e:
        print("Error during scraping:")
        traceback.print_exc()
    finally:
        driver.quit()

# Example usage
"""if __name__ == "__main__":
    example_url = "https://www.hltv.org/results"
    scrape_links_and_next_page(example_url)"""