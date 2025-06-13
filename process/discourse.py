import os
import re
from markdownify import markdownify as md

INPUT_DIR = "data/discourse"   # directory where .txt files are saved
OUTPUT_DIR = "data/md"   # directory for new .md files

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def process_txt_file(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract metadata
    title_match = re.search(r"^Title:\s*(.+)", content, re.MULTILINE)
    user_match = re.search(r"^User:\s*(.+)", content, re.MULTILINE)
    url_match = re.search(r"^URL:\s*(.+)", content, re.MULTILINE)

    title = title_match.group(1).strip() if title_match else "Untitled"
    user = user_match.group(1).strip() if user_match else "unknown"
    url = url_match.group(1).strip() if url_match else ""

    # Extract cooked HTML (everything after the URL line)
    cooked_html = content.split("URL:", 1)[-1].split("\n", 1)[-1].strip()

    # Convert to markdown
    markdown_body = md(cooked_html, heading_style="ATX")

    # Create .md file
    filename = sanitize_filename(title) + ".md"
    md_path = os.path.join(OUTPUT_DIR, filename)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"**User**: {user}\n")
        f.write(f"**URL**: [{url}]({url})\n\n")
        f.write(markdown_body.strip() + "\n")

    print(f"[✔] Converted: {txt_path} → {md_path}")

# Process all .txt files
for file in os.listdir(INPUT_DIR):
    if file.endswith(".txt"):
        process_txt_file(os.path.join(INPUT_DIR, file))

print(f"\n✅ All .txt files converted to Markdown in: {OUTPUT_DIR}")
