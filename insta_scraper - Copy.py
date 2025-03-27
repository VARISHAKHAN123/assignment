import requests
from bs4 import BeautifulSoup
import csv
import logging
import os

# Ensure 'logs' and 'data' directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Setup logging
logging.basicConfig(filename="logs/insta_scraper.log", level=logging.INFO)

INSTAGRAM_URL = "https://www.instagram.com/bbcnews/"

def fetch_instagram_post():
    try:
        response = requests.get(INSTAGRAM_URL)
        if response.status_code != 200:
            logging.error(f"Failed to fetch page. Status Code: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract caption and image URL (simplified example)
        caption = soup.find("meta", property="og:title")
        image_url = soup.find("meta", property="og:image")

        if caption and image_url:
            return {"caption": caption["content"], "image_url": image_url["content"]}
        else:
            logging.warning("No post data found!")
            return None

    except Exception as e:
        logging.error(f"Error fetching Instagram post: {e}")
        return None

def save_to_csv(data):
    with open("data/instagram_post.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Caption", "Image URL"])
        writer.writerow([data["caption"], data["image_url"]])

if __name__ == "__main__":
    post_data = fetch_instagram_post()
    if post_data:
        print(f"Latest Post:\nCaption: {post_data['caption']}\nImage URL: {post_data['image_url']}")
        save_to_csv(post_data)
        print("Data saved to instagram_post.csv!")
    else:
        print("No post data found!")
