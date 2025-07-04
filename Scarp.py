from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup Selenium options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# Path to your ChromeDriver (adjust if needed)
service = Service()
driver = webdriver.Chrome(service=service, options=options)

all_jobs = []

# Loop through pages
for page in range(1, 4):
    url = f"https://internshala.com/internships/page-{page}/"
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    internships = soup.find_all("div", class_="individual_internship")

    print(f"✅ Page {page} - Jobs found: {len(internships)}")

    for job in internships:
        # Skip ads or offers
        if "Enroll now" in job.get_text() or "OFFER" in job.get_text():
            continue

        # Extract Title
        title_tag = job.find("a", class_="job-title-href")
        title = title_tag.text.strip() if title_tag else "N/A"

        # Extract Company
        company_tag = job.find("p", class_="company-name")
        company = company_tag.text.strip() if company_tag else "N/A"

        # Extract Location
        location_tag = job.find("div", class_="location_link")
        if not location_tag:
            location_tag = job.find("div", class_="row-1-item locations")
        location = location_tag.text.strip() if location_tag else "N/A"

        # Extract Skills
        skill_section = job.find("div", class_="other_detail_item", string=lambda x: x and "Skill(s) required" in x)
        skills = skill_section.find_next_sibling("div").text.strip() if skill_section else "N/A"

        all_jobs.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Skills": skills
        })

driver.quit()

# Convert to DataFrame
df = pd.DataFrame(all_jobs)

# If no jobs were scraped
if df.empty:
    print("⚠️ No valid jobs found. Skipping CSV export and plots.")
else:
    # Save to CSV
    df.to_csv("internshala_jobs.csv", index=False)
    print(f"\n✅ Total Jobs Scraped: {len(df)}")
    print(df.head())

    # Plot skills
    df_skills = df[df["Skills"] != "N/A"].copy()
    if not df_skills.empty:
        all_skills = ", ".join(df_skills["Skills"].tolist()).split(",")
        all_skills = [skill.strip() for skill in all_skills if skill.strip()]
        skill_counts = pd.Series(all_skills).value_counts().head(10)

        plt.figure(figsize=(10, 5))
        sns.barplot(x=skill_counts.values, y=skill_counts.index, palette="viridis")
        plt.title("Top 10 Skills Required in Internships")
        plt.xlabel("Number of Listings")
        plt.ylabel("Skills")
        plt.tight_layout()
        plt.show()
    else:
        print("⚠️ No skills data to plot.")

    # Plot locations
    df_location = df[df["Location"] != "N/A"]
    if not df_location.empty:
        location_counts = df_location["Location"].value_counts().head(10)
        plt.figure(figsize=(10, 5))
        sns.barplot(x=location_counts.values, y=location_counts.index, palette="coolwarm")
        plt.title("Top 10 Internship Locations")
        plt.xlabel("Number of Listings")
        plt.ylabel("Location")
        plt.tight_layout()
        plt.show()
    else:
        print("⚠️ No job locations to plot.")
