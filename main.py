from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import random

url = 'https://hamrobazaar.com/category/cars/EB9C8147-07C0-4951-A962-381CDB400E37/F93D355F-CC20-4FFE-9CB7-6C7CDFF1DC50'
 
chrome_driver_path = 'C:/Users/rijal/OneDrive/Desktop/Web_Scraping/chromedriver.exe'

service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# List to store the scraped car data and a set to keep track of processed listings
cars_data = []
processed_ids = set()

# Variables to control the scraping attempts
attempt = 0
max_attempts = 15

def get_comments(link):
    """
    Scrape comments from an individual car page.
    
    This function opens a new window, navigates to the car's page,
    waits for comments to load, scrolls the page to ensure all comments 
    are visible, then collects and returns the comments.
    
    If any error occurs (for example, comments not found), it returns an empty list.
    """
    try:
        # Save the current window so we can return to it later
        original_window = driver.current_window_handle
        
        # Open a new window and navigate to the car's page
        driver.switch_to.new_window('window')
        driver.get(link)
        
        comments = []
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article.comment--body"))
            )
            
            # Scroll down a couple of times to load comments dynamically
            for _ in range(2):
                driver.execute_script("window.scrollBy(0, 300)")
                time.sleep(random.uniform(0.5, 1.0))
            
            comment_elements = driver.find_elements(By.CSS_SELECTOR, "p.user__text")
            comments = [comment.text.strip() for comment in comment_elements]
            
        except Exception as inner_error:
            print(f"Comments not found: {str(inner_error)[:60]}")
        
        finally:
            # Close the new window and switch back to the original window
            driver.close()
            driver.switch_to.window(original_window)
            time.sleep(random.uniform(1.0, 2.0))
        
        return comments
    
    except Exception as error:
        print(f"Failed to process comments: {str(error)[:60]}")
        return []

try:
    driver.get(url)

    # Continue scraping until we have at least 60 listings or we reach the maximum number of attempts
    while len(cars_data) < 60 and attempt < max_attempts:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-list"))
        )
        
        listings = driver.find_elements(By.CSS_SELECTOR, "div.card-product-linear")
        print(f"Found {len(listings)} listings on attempt {attempt + 1}")
        
        # Loop through each listing and extract information
        for listing in listings:
            try:
                # Use data-id attribute if available, otherwise fallback to the listing's internal id
                listing_id = listing.get_attribute("data-id") or listing.id
                # Skip the listing if it has already been processed
                if listing_id in processed_ids:
                    continue
                
                # Extract details from the listing
                title = listing.find_element(By.CSS_SELECTOR, "h2.product-title").text.strip()
                user = listing.find_element(By.CSS_SELECTOR, "span.username-fullname").text.strip()
                link = listing.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                price = listing.find_element(By.CSS_SELECTOR, "span.regularPrice").text.strip()
                condition = listing.find_element(By.CSS_SELECTOR, "span.condition").text.strip()
                location = listing.find_element(By.CSS_SELECTOR, "span.location").text.strip()
                details = listing.find_element(By.CSS_SELECTOR, "p.description").text.strip()
                
                # Get comments from the individual car page
                comments = get_comments(link) if link else []
                
                # Add the extracted information to our list
                cars_data.append({
                    "Title": title,
                    "User": user,
                    "Price": price,
                    "Condition": condition,
                    "Location": location,
                    "Details": details,
                    "Comments": comments
                })
                # Mark this listing as processed
                processed_ids.add(listing_id)
                print(f"Processed {len(cars_data)}: {title[:30]}...")
                
                # If we have reached the desired number of listings, break out of the loop
                if len(cars_data) >= 60:
                    break
                    
            except Exception as e:
                print(f"Skipped listing: {str(e)[:60]}")
                continue

        # Scroll down the page to load more listings
        scroll_amount = random.randint(800, 1200)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(2.0, 3.5))
        
        # Occasionally scroll up a bit to mimic natural scrolling behavior
        if random.random() < 0.25:
            driver.execute_script("window.scrollBy(0, -200)")
            time.sleep(0.5)
            
        attempt += 1
        
finally:
    driver.quit()

# Save the collected data into a CSV file
with open("car_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Title", "User","Price" ,"Condition" ,"Location", "Details", "Comments"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write each listing's data into the CSV file
    for entry in cars_data:
        writer.writerow({
            "Title": entry["Title"],
            "User": entry["User"],
            "Price": entry["Price"],
            "Condition": entry["Condition"],
            "Location": entry["Location"],
            "Details": entry["Details"],
            "Comments": " | ".join(entry["Comments"]) if entry["Comments"] else "--No Comments--"
        })

print(f"Successfully scraped {len(cars_data)} listings with comments!")
