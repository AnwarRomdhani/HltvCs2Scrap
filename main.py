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
    Scrape the first match row from HLTV results.
    """
    driver = setup_edge_driver()
    url = "https://www.hltv.org/results?offset=0"
    
    try:
        # Open the target URL
        driver.get(url)
        time.sleep(random.uniform(5, 10))  # Mimic human browsing
        
        # Locate the specific <tr> element using XPath
        tr_xpath = "//table/tbody/tr"  # Use a relative XPath for better reliability
        tr_element = driver.find_element(By.XPATH, tr_xpath)
        
        # Extract text from all child elements of <tr>, ignoring <img> tags
        child_elements = tr_element.find_elements(By.XPATH, "./*")  # Find all direct children
        for child in child_elements:
            if child.tag_name != "img":  # Ignore images
                print(child.text.strip())  # Print the text content of each child

    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_match_row()
