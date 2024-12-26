# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator
from collections import Counter
import os
import time

# BrowserStack credentials
username = os.getenv('asthasuman_yjSCG8')  # Use environment variables for security
access_key = os.getenv('qQ2wQgL7UcYoyvq7yqnE')

# Define desired capabilities for BrowserStack
desired_capabilities = {
    'browser': 'Chrome',  # You can change this to 'Firefox', 'Edge', etc.
    'browser_version': 'latest',
    'os': 'Windows',
    'os_version': '10',
    'name': 'Opinion Section Scraping Test',  # Test name
    'build': '1.0',  # Build name
}

# Initialize the WebDriver to connect to BrowserStack
driver = webdriver.Remote(
    command_executor='https://hub-cloud.browserstack.com/wd/hub',
    options=webdriver.ChromeOptions(),
    desired_capabilities=desired_capabilities,
    keep_alive=True
)

# List of article URLs to scrape
article_links = [
    "https://elpais.com/opinion/2024-12-24/felipe-vi-la-exigencia-del-bien-comun.html",
    "https://elpais.com/opinion/2024-12-24/el-ano-de-sanchez.html",
    "https://elpais.com/opinion/2024-12-25/lo-admito-la-tierra-es-esferica.html",
    "https://elpais.com/opinion/2024-12-25/el-gobierno-de-los-millonarios.html",
    "https://elpais.com/opinion/2024-12-25/milagro-en-el-atasco.html"
]

# Initialize a list to store article data
articles_data = []

# Scrape the articles
for link in article_links:
    try:
        driver.get(link)
        
        # Wait for the title to be present
        title = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))  # Title in <h1>
        ).text
        
        # Wait for the subtitle to be present
        subtitle = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))  # Subtitle in <h2>
        ).text
        
        # Wait for the content to be present
        content = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a_c"))  # Adjusted class name
        ).text
        
        # Store the article data
        articles_data.append({
            "title": title,
            "subtitle": subtitle,
            "link": link,
            "content": content
        })

        # Additional wait time to ensure the page is fully loaded
        time.sleep(5)  # Increased wait time after loading each article

    except Exception as e:
        print(f"Error processing article {link}: {e}")

# Close the WebDriver
driver.quit()

# Print the scraped articles data
for article in articles_data:
    print(f"Título: {article['title']}\nSubtítulo: {article['subtitle']}\nEnlace: {article['link']}\nContenido: {article['content']}\n")


# Step 3: Translate Article Headers
# Initialize the translator
translator = GoogleTranslator()

# Translate titles and subtitles
for article in articles_data:
    try:
        if article['title'] and article['subtitle']:  # Check if title and subtitle are not empty
            translated_title = translator.translate(article['title'], source='es', target='en')
            translated_subtitle = translator.translate(article['subtitle'], source='es', target='en')
            article['translated_title'] = translated_title
            article['translated_subtitle'] = translated_subtitle
        else:
            article['translated_title'] = "No title available"
            article['translated_subtitle'] = "No subtitle available"
    except Exception as e:
        print(f"Error translating article {article['link']}: {e}")
        article['translated_title'] = "Translation error"
        article['translated_subtitle'] = "Translation error"

# Print the translated articles data
for article in articles_data:
    print(f"Original Title: {article['title']}\nTranslated Title: {article['translated_title']}")
    print(f"Original Subtitle: {article['subtitle']}\nTranslated Subtitle: {article['translated_subtitle']}\n")

# Step 4: Analyze Translated Headers
# Collect all translated titles and subtitles
all_translated_texts = [article['translated_title'] for article in articles_data] + \
                        [article['translated_subtitle'] for article in articles_data]

# Count word occurrences
word_count = Counter()
for text in all_translated_texts:
    words = text.split()
    word_count.update(words)

# Identify repeated words
repeated_words = {word: count for word, count in word_count.items() if count > 2}
print("Repeated words in translated headers:", repeated_words)