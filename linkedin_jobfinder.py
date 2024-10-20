import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from tqdm import tqdm  # Progress bar

class LinkedInJobScraper:
    def __init__(self, config_path, driver_path):
        # Load credentials from config file
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.username = config['username']
        self.password = config['password']
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.jobs = []
        self.total_jobs_considered = 0
        self.total_jobs_chosen = 0

    def login(self):
        # Open LinkedIn login page
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        # Log in
        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for login to complete

    def search_jobs(self, location, experience_levels=["Mid-Senior"], date_posted="Past Week", search_query="relocation work visa sponsorship"):
        # Navigate to LinkedIn Jobs page
        self.driver.get("https://www.linkedin.com/jobs/")
        time.sleep(2)

        # Search for jobs with the specific query
        search_box = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search jobs']")
        search_box.clear()
        search_box.send_keys(search_query)

        # Search by location
        location_box = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search location']")
        location_box.clear()
        location_box.send_keys(location)
        location_box.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for the results to load

        # Apply multiple experience levels
        self.apply_experience_level_filter(experience_levels)
        
        # Apply date posted filter
        self.apply_date_posted_filter(date_posted)

    def apply_experience_level_filter(self, experience_levels):
        # Apply the experience level filters based on the input list (e.g., Mid-Senior, Director, Executive, etc.)
        try:
            experience_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Experience Level filter. Clicking this button displays all Experience Level filter options.']")
            experience_button.click()
            time.sleep(1)

            # Loop through each experience level and apply the filter
            for experience_level in experience_levels:
                experience_option = self.driver.find_element(By.XPATH, f"//span[text()='{experience_level}']")
                experience_option.click()
                time.sleep(1)

            # Close the filter dropdown after selecting the options
            self.driver.find_element(By.XPATH, "//button[@aria-label='Apply current filters']").click()
            time.sleep(2)
        except Exception as e:
            print(f"Error applying experience level filter: {e}")

    def apply_date_posted_filter(self, date_posted):
        # Apply the date posted filter based on the input (e.g., "Past 24 hours", "Past Week")
        try:
            date_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Date Posted filter. Clicking this button displays all Date Posted filter options.']")
            date_button.click()
            time.sleep(1)
            
            # Match the date posted filter
            date_option = self.driver.find_element(By.XPATH, f"//span[text()='{date_posted}']")
            date_option.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error applying date posted filter ({date_posted}): {e}")

    def scrape_jobs(self, location):
        jobs_in_location = 0
        jobs_chosen_in_location = 0
        page = 1

        while True:
            # Get job postings on the current page
            job_cards = self.driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
            jobs_in_location += len(job_cards)

            for job in tqdm(job_cards, desc=f"Scraping jobs in {location} (Page {page})"):
                title = job.find_element(By.CSS_SELECTOR, ".job-card-list__title").text
                company = job.find_element(By.CSS_SELECTOR, ".job-card-container__company-name").text
                location_text = job.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-item").text
                job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                # Add only jobs that meet specific criteria (e.g., visa sponsorship)
                if "visa" in title.lower() or "sponsorship" in title.lower():
                    self.jobs.append({
                        "title": title,
                        "company": company,
                        "location": location_text,
                        "link": job_link
                    })
                    jobs_chosen_in_location += 1

            # Move to the next page if available
            try:
                next_button = self.driver.find_element(By.CLASS_NAME, "next-button")
                next_button.click()
                page += 1
                time.sleep(5)  # Wait for the next page to load
            except Exception as e:
                print(f"No more pages to scrape for {location}.")
                break

        # Update totals for jobs considered and chosen
        self.total_jobs_considered += jobs_in_location
        self.total_jobs_chosen += jobs_chosen_in_location

        # Display the number of jobs considered and chosen in this location
        print(f"\nFinished scraping {location}.")
        print(f"Jobs considered: {jobs_in_location}, Jobs chosen: {jobs_chosen_in_location}\n")

    def export_to_csv(self, filename="linkedin_jobs.csv"):
        # Export the scraped jobs to a CSV file
        df = pd.DataFrame(self.jobs)
        df.to_csv(filename, index=False)
        print(f"Exported data to {filename}")

    def export_to_excel(self, filename="linkedin_jobs.xlsx"):
        # Export the scraped jobs to an Excel file
        df = pd.DataFrame(self.jobs)
        df.to_excel(filename, index=False)
        print(f"Exported data to {filename}")

    def quit(self):
        # Quit the driver
        self.driver.quit()

# Main program
if __name__ == "__main__":
    from time import time as timer  # For tracking elapsed time

    # Set paths for config and WebDriver
    CONFIG_PATH = "config.json"  # Path to configuration file
    DRIVER_PATH = "/./chromedriver"  # Path to WebDriver

    # Create an instance of LinkedInJobScraper
    scraper = LinkedInJobScraper(CONFIG_PATH, DRIVER_PATH)

    # Start the timer
    start_time = timer()

    print('Welcome to LinkedIn Job Finder (Estratek)!')

    # Log in to LinkedIn
    scraper.login()

    # Define locations and filters for the job search
    locations = [
        "Venezuela", "Latin America", "Germany", "Spain", "UK", "Ireland", 
        "Netherlands", "United States", "Canada"
    ]

    experience_levels = ["Mid-Senior", "Director"]  # Multiple experience levels
    date_posted = "Past Week"

    # Search and scrape jobs for each location
    for loc in locations:
        scraper.search_jobs(loc, experience_levels=experience_levels, date_posted=date_posted)
        scraper.scrape_jobs(loc)

    # Export the results to CSV and Excel
    scraper.export_to_csv("linkedin_jobs.csv")
    scraper.export_to_excel("linkedin_jobs.xlsx")

    # Stop the timer
    end_time = timer()
    elapsed_time = end_time - start_time

    # Summary of totals
    print("\n=== Summary ===")
    print(f"Total jobs considered: {scraper.total_jobs_considered}")
    print(f"Total jobs chosen: {scraper.total_jobs_chosen}")
    print(f"Total time elapsed: {elapsed_time:.2f} seconds")

    # Close the browser
    scraper.quit()
