import csv
import os  # To check if the file exists
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

def scrape_teams_box(driver, wait):
    """
    Scrape the content of the <div> with class 'standard-box teamsBox' (excluding images).
    """
    try:
        print("\nWaiting for the teams box to load...")
        teams_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".standard-box.teamsBox"))
        )
        print("Teams box found. Scraping content...")
        return teams_box.text.strip()
    except Exception as e:
        print("Error while scraping teams box:")
        traceback.print_exc()
        return ""

def scrape_maps_div(driver, wait):
    """
    Scrape the content of the <div> with class 'box-headline flexbox nowrap header'.
    """
    try:
        print("\nWaiting for the maps div to load...")
        maps_div = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".box-headline.flexbox.nowrap.header"))
        )
        print("Maps div found. Scraping content...")
        return maps_div.text.strip()
    except Exception as e:
        print("Error while scraping maps div:")
        traceback.print_exc()
        return ""

def extract_match_metadata(teams_box_content):
    """
    Extract match metadata: match name, winning team, losing team, and score.
    """
    lines = teams_box_content.split("\n")
    match_name = lines[4] if len(lines) > 4 else "Unknown Match"
    winning_team = lines[-2] if len(lines) > 1 else "Unknown Team"
    losing_team = lines[0] if len(lines) > 0 else "Unknown Team"
    score = f"{lines[-1]} - {lines[1]}" if len(lines) > 1 else "Unknown Score"  # Format: "Winning score - Losing score"
    return match_name, winning_team, losing_team, score

def save_to_csv(match_name, winning_team, losing_team, score, maps, tables_data, filename):
    """
    Save match metadata, maps, and player statistics to a structured CSV file.
    Append data if the file already exists.
    """
    file_exists = os.path.isfile(filename)  # Check if the file exists

    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write headers only if the file is being created
            if not file_exists:
                # Metadata Header
                writer.writerow(["Match", "Winning Team", "Losing Team", "Score", "Maps Played"])
                # Player Stats Header
                writer.writerow(["Team", "Player Name", "K-D", "+/-", "ADR", "KAST", "Rating"])

            # Write match metadata
            writer.writerow([match_name, winning_team, losing_team, score, maps])

            # Write player statistics
            for table_index, (team_name, rows) in tables_data.items():
                for row in rows:
                    writer.writerow([team_name] + row)

            print(f"Data appended to {filename}")
    except Exception as e:
        print("Error saving to CSV:")
        traceback.print_exc()

def scrape_match_data(url):
    """
    Scrape match data from the given URL, including teams, scores, maps, and player performance.
    """
    driver = setup_edge_driver()
    tables_data = {}

    try:
        # Open the target URL
        driver.get(url)

        # Wait for the page to load
        wait = WebDriverWait(driver, 20)  # Adjust timeout as needed

        # Scrape the teams box content
        teams_box_content = scrape_teams_box(driver, wait)
        match_name, winning_team, losing_team, score = extract_match_metadata(teams_box_content)

        # Scrape the maps information
        maps_info = scrape_maps_div(driver, wait)

        print("\nWaiting for tables to load...")
        # Locate all tables with the desired classes
        tables = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".table.totalstats")))
        print(f"Found {len(tables)} tables.")

        # Scrape data from each table
        for table_index, table in enumerate(tables, start=1):
            print(f"\nScraping Table {table_index}:")
            rows = table.find_elements(By.TAG_NAME, "tr")
            team_name = rows[0].find_elements(By.TAG_NAME, "td")[0].text if rows else "Unknown Team"
            table_data = []

            for row_index, row in enumerate(rows[1:], start=2):  # Skip the header row
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    cell_texts = [cell.text.strip() for cell in cells]
                    table_data.append(cell_texts)
                    print(f"Row {row_index}: {cell_texts}")

            tables_data[f"Table {table_index}"] = (team_name, table_data)

        # Save all the scraped data to a CSV file
        filename = "match_data.csv"
        save_to_csv(match_name, winning_team, losing_team, score, maps_info, tables_data, filename)

    except Exception as e:
        print("Error during scraping:")
        traceback.print_exc()
    finally:
        driver.quit()

"""if __name__ == "__main__":
    # Example usage of the function
    match_url = "https://www.hltv.org/matches/2378056/shimmer-vs-lotus-fe-esl-impact-autumn-2024-cash-cup-6-north-america"
    scrape_match_data(match_url) """
