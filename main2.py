#Sheffa Kochay
#SDET 101
#February 24, 2025

#7

import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
import nltk
import re
from dotenv import load_dotenv
import os

import ssl
import nltk
ssl._create_default_https_context = ssl._create_unverified_context
nltk.download("stopwords")

# Load environment variables from .env file
load_dotenv()

# Ensure NLTK stopwords are downloaded
nltk.download("stopwords")

# Get NewsAPI key from environment variable
API_KEY = os.getenv("NEWS_API_KEY")
CATEGORY = "technology"  # Replace with any category (e.g., health, business)

if not API_KEY:
    raise ValueError("API_KEY not found. Please ensure the .env file contains NEWS_API_KEY.")

# Fetch from NewsAPI
url = f"https://newsapi.org/v2/top-headlines?category={CATEGORY}&apiKey={API_KEY}"
response = requests.get(url)
data = response.json()

# Extract article titles
articles = data.get("articles", [])
titles = [article["title"] for article in articles if article["title"]]

# Preprocess text: Remove special characters and stop words
stop_words = set(stopwords.words("english"))
words = []

for title in titles:
    title = re.sub(r"[^a-zA-Z\s]", "", title)  # Remove special characters
    for word in title.lower().split():
        if word not in stop_words:
            words.append(word)

# word frequency analysis
word_freq = Counter(words)

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)

# Plot word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title(f"Most Common Words in {CATEGORY.capitalize()} News Headlines")
plt.show()

# Analysis of main topics based on word frequencies:
# The most common words in the headlines can show us the main topics in the news right now.
# For example, if words like "AI", "technology", "innovation", or "startup" appear often, it may mean there’s a lot of focus on new tech and businesses.
# If words like "health", "medicine", "pandemic", or "research" are common, the news might be focusing on health issues.
# By looking at these words, we can understand what people are talking about in the news and what’s happening in the world.
