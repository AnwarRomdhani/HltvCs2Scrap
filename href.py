from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import random

def setup_edge_driver():
    """
    Set up Microsoft Edge WebDriver.
    """
    # Specify the path to the Edge WebDriver executable
    edge_driver_path = r"Driver_Notes\msedgedriver.exe"  # Adjust to your actual path
    
    # Initialize the Edge driver
    driver = webdriver.Edge(service=Service(edge_driver_path))
    return driver

def scrape_match_row():
    """
    Scrape the first match row from HLTV results by extracting the direct link from the <a> tag.
    """
    driver = setup_edge_driver()
    url = "https://www.hltv.org/results?offset=0"
    
    try:
        # Open the target URL
        driver.get(url)
        time.sleep(random.uniform(5, 10))  # Mimic human browsing
        
        # Locate the specific <a> element using a more accurate XPath
        a_xpath = "//div[@class='result-con']/a"
        a_element = driver.find_element(By.XPATH, a_xpath)
        
        # Extract the href attribute from the <a> tag
        match_link = a_element.get_attribute("href")
        print(f"Extracted Match Link: {match_link}")
        
        # Navigate to the extracted link directly
        driver.get(match_link)
        time.sleep(random.uniform(5, 10))  # Wait for the match details page to load

        # Example: Scrape some details from the match details page
        print("Scraping match details...")
        details_xpath = "//div[contains(@class, 'match-info-box')]"
        match_details = driver.find_elements(By.XPATH, details_xpath)
        for detail in match_details:
            print(detail.text.strip())
            
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_match_row()
