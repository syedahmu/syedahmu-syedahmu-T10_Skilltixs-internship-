# syedahmu-syedahmu-T10_Skilltixs-internship-
# 📝 Internshala Internship Scraper

A Python script that scrapes internship listings from Internshala, saves the results to CSV, and visualizes the top skills and locations using Pandas, Matplotlib, and Seaborn.

---

## 🚀 Features

- Headless Selenium browsing to load dynamic content
- Parsing with BeautifulSoup
- Extracts internship **Title**, **Company**, **Location**, and **Skills**
- Saves results to `internshala_jobs.csv`
- Visualizes:
  - Top 10 skills across listings
  - Top 10 internship locations

---

## ⚙️ Requirements

- Python 3.7+
- Chrome (latest version)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (must match Chrome version)
- Python packages:
  ```bash
  pip install selenium beautifulsoup4 pandas matplotlib seaborn
