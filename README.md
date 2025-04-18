```markdown
# 📧 Email Scraper

This Python script visits a website, scrapes any email addresses it finds, and saves them to a CSV file named `emails.csv`.

---

## 📁 How to Use

### 1. Download the Code

Clone this repository or [Download as ZIP](https://github.com/Mavon2309/simple-scraper-main) and unzip it:

```bash
git clone https://github.com/Mavon2309/simple-scraper-main
cd simple-scraper-main
```

To use it, you will need to run:

```bash
pip install requests beautifulsoup4
```

After running the scraper (which might take some time), you will need to update the following code at the bottom to whichever website you want to run it for. It won't run properly for all websites, and I will try and update the code to make it work for more websites:

```python
if __name__ == '__main__':
    start_url = 'https://www.example.com/'
    scrape_website(start_url)
```

To run the script, you just need to use:

```bash
python scraper.py
```
```

This will ensure that all of your code snippets are properly formatted in code blocks!
