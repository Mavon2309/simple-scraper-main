import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time
import csv
import os

# Browser-like headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

MAX_DEPTH = 2  # How deep the scraper should go

def get_emails_from_text(text):
    return re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)

def parse_name_from_email(email):
    name_part = email.split("@")[0]
    parts = re.split(r'[._\-]', name_part)
    capitalized_parts = [p.capitalize() for p in parts if p.isalpha()]
    return " ".join(capitalized_parts) if capitalized_parts else "Unknown"

def fetch_page(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            start = time.time()
            response = requests.get(url, headers=HEADERS, timeout=15)
            elapsed = time.time() - start
            return response, elapsed
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            time.sleep(delay)
    return None, 0

def scrape_website(start_url):
    start_time = time.time()  # Start overall timing

    domain = urlparse(start_url).netloc
    visited = set()
    found_emails = {}
    to_visit = [(start_url, 0)]  # (URL, depth)

    slowest_url = ""
    slowest_time = 0

    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > MAX_DEPTH:
            continue

        visited.add(url)
        print(f"🌐 Visiting (depth {depth}): {url}")
        response, load_time = fetch_page(url)
        if not response:
            continue

        # Track the slowest page
        if load_time > slowest_time:
            slowest_time = load_time
            slowest_url = url

        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()
        for email in get_emails_from_text(page_text):
            found_emails[email] = parse_name_from_email(email)

        # Collect internal links for deeper crawling
        if depth < MAX_DEPTH:
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                if urlparse(full_url).netloc == domain and full_url not in visited:
                    to_visit.append((full_url, depth + 1))

    # Write results to CSV
    output_file = "emails.csv"
    if found_emails:
        with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Email"])
            for email, name in sorted(found_emails.items()):
                writer.writerow([name, email])
        print(f"\n✅ Saved {len(found_emails)} emails to '{output_file}'")

        # Automatically open the CSV file (Windows only)
        os.startfile(output_file)
    else:
        print("❌ No emails found.")

    total_time = time.time() - start_time
    print(f"\n⏱️ Completed in {total_time:.2f} seconds.")
    if slowest_url:
        print(f"🐢 Slowest page: {slowest_url} ({slowest_time:.2f} seconds)")

if __name__ == '__main__':
    start_url = 'https://www.burnsmcd.com/'
    scrape_website(start_url)
