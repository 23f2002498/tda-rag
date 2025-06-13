import os
import time
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.sync_api import sync_playwright

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text.strip())[:80]

def strip_html(html):
    return BeautifulSoup(html, "html.parser").get_text()

CATEGORY_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"
OUTPUT_DIR = "data/discourse"
allowed_users = {"jivraj", "HritikRoshan_HRM", "iamprasna", "carlton"}
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_json_url(topic_url):
    parts = topic_url.split("/")
    topic_slug = parts[4]
    topic_id = parts[5]
    return f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_slug}/{topic_id}.json"

def save_post(post, topic_slug, topic_title):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    post_number = post.get("post_number", 1)
    topic_id = post.get("topic_id", "unknown")
    filename = f"{sanitize_filename(topic_slug)}-{post_number}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    post_url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_slug}/{topic_id}/{post_number}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Title: {topic_title}\n")
        f.write(f"User: {post['username']}\n")
        f.write(f"URL: {post_url}\n\n")
        f.write(post["cooked"])
    
    print(f"[SAVE] {filepath} (user: {post['username']})")

def scroll_to_bottom(page, max_scrolls=50):
    for _ in range(max_scrolls):
        previous_height = page.evaluate("document.body.scrollHeight")
        page.mouse.wheel(0, 9999)
        time.sleep(1)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
    print("[INFO] Finished scrolling, all topics loaded.")

def scrape():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="auth_profile",
            headless=False
        )
        page = context.new_page()
        print("[INFO] Loading category page… login if needed.")
        page.goto(CATEGORY_URL)
        page.wait_for_selector("a.title.raw-link.raw-topic-link", timeout=60000)

        scroll_to_bottom(page)

        topic_links = page.eval_on_selector_all(
            "a.title.raw-link.raw-topic-link",
            "els => els.map(el => ({ href: el.href, text: el.innerText }))"
        )

        print(f"[INFO] Found {len(topic_links)} topics.")

        for topic in topic_links:
            topic_url = topic["href"]
            print(f"[INFO] Visiting topic: {topic_url}")

            json_url = get_json_url(topic_url)
            print(f"[INFO] Fetching JSON from: {json_url}")

            try:
                page.goto(json_url)
                page.wait_for_selector("pre", timeout=10000)
                raw_json = page.locator("pre").inner_text()
                data = json.loads(raw_json)

                posts = data.get("post_stream", {}).get("posts", [])
                topic_slug = data.get("slug", "unknown-slug")
                topic_id = str(data.get("id", "unknown-id"))

                for post in posts:
                    if post.get("username") not in allowed_users:
                        continue
                    post["topic_id"] = topic_id
                    save_post(post, topic_slug, data.get("title", "Untitled"))

            except Exception as e:
                print(f"[WARN] Failed to parse {json_url}: {e}")

            time.sleep(1)

        print(f"[DONE] All posts saved to {OUTPUT_DIR}")

scrape()
