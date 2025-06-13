import os
import re
from markdownify import markdownify as md
from bs4 import BeautifulSoup

INPUT_DIR = "data/tds"
OUTPUT_DIR = "data/md"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def remove_pagination_blocks(html):
    soup = BeautifulSoup(html, "html.parser")
    # Remove pagination blocks that contain "Previous" or "Next"
    for div in soup.find_all("div", class_=re.compile(r"pagination-item")):
        label = div.find("span")
        if label and label.get_text(strip=True) in ("Previous", "Next"):
            div.decompose()
    return str(soup)

def convert_html_to_md(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Clean pagination
    cleaned_html = remove_pagination_blocks(html)

    # Convert to markdown
    markdown_text = md(cleaned_html, heading_style="ATX")

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    base_name = sanitize_filename(base_name)
    md_path = os.path.join(OUTPUT_DIR, base_name + ".md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_text.strip() + "\n")

    print(f"[✔] Converted: {file_path} → {md_path}")

# Run for all .html files
for file in os.listdir(INPUT_DIR):
    if file.lower().endswith(".html"):
        convert_html_to_md(os.path.join(INPUT_DIR, file))

print(f"\n✅ All cleaned Markdown files saved in: {OUTPUT_DIR}")
