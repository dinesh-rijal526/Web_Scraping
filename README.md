# Web_Scraping
 
# Web Scraping: Car Listings from Hamro Bazaar

## Project Overview
This script scrapes car listings from [Hamro Bazaar](https://hamrobazaar.com) to collect details such as title, price, condition, location, description, and comments. The data is stored in a CSV file (`car_data.csv`). The goal is to collect **50+ listings** .

---

## Key Features
- **Automated Scraping**: Uses Selenium to simulate browser interactions.
- **Comment Extraction**: Opens individual listing pages to scrape user comments.
- **Duplicate Prevention**: Tracks processed listings using unique IDs.
- **Dynamic Loading**: Handles infinite scroll via randomized scrolling.
- **Error Resilience**: Skips failed listings gracefully and logs errors.

---

## Prerequisites
1. **Python Libraries**:
   - `selenium` (for browser automation)
   - `csv` (for data export)
   ```bash
   pip install selenium
