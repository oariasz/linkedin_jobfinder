![LinkedIn Logo](https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png)

# LinkedIn Job Scraper

This project is a Python-based web scraper designed to collect job opportunities from LinkedIn based on specified filters, such as **locations**, **job types**, **experience levels**, and **posting dates**. The scraper is built using Selenium for browser automation and includes features like real-time progress tracking and export capabilities to CSV and Excel formats.

## Features
- **Location-based scraping**: The scraper extracts job listings from specific countries and regions.
- **Job type filtering**: Supports filtering jobs by on-site or hybrid types.
- **Relocation support**: Filters jobs based on employers willing to support relocation or provide visa sponsorship.
- **Multiple experience levels**: Specify one or more experience levels (e.g., Mid-Senior, Director, Executive).
- **Posting date filtering**: Filter jobs based on how recently they were posted (e.g., "Past 24 hours", "Past Week").
- **Progress tracking**: Shows live scraping progress in the console using `tqdm`.
- **Data export**: Export scraped jobs to both CSV and Excel formats.

## Requirements

### Software:
- Python 3.8+
- Selenium WebDriver (ChromeDriver or equivalent)
- Google Chrome browser (or the browser of your choice)
  
### Python Libraries:
- `selenium`
- `pandas`
- `tqdm`

Install the required libraries with:
```bash
pip install selenium pandas tqdm
