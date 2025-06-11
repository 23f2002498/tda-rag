import requests
from bs4 import BeautifulSoup
import os
import re
from playwright.sync_api import sync_playwright

BASE_URL = "https://tds.s-anand.net/"

def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "_", title)

def scrape(html,title):
    try:
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find('article', id='main')
        if not article:
            print(f"[!] Skipping (no content): {title}")
            return
        text = str(article)
        os.makedirs("data/tds", exist_ok=True)
        filename = os.path.join("data/tds", sanitize_filename(title) + ".html")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"[✓] Saved: {filename}")
    except Exception as sub_e:
        print(f"[✗] Error scraping '{title}': {sub_e}")


all_links = [
    ("Home","#/"),
    ("Tools in Data Science", "#/README"),
    ("1. Development Tools", "#/development-tools"),
    ("Editor: VS Code", "#/vscode"),
    ("AI Code Editors: GitHub Copilot", "#/github-copilot"),
    ("Python tools: uv", "#/uv"),
    ("JavaScript tools: npx", "#/npx"),
    ("Unicode", "#/unicode"),
    ("Browser: DevTools", "#/devtools"),
    ("CSS Selectors", "#/css-selectors"),
    ("JSON", "#/json"),
    ("Terminal: Bash", "#/bash"),
    ("AI Terminal Tools: llm", "#/llm"),
    ("Spreadsheet: Excel, Google Sheets", "#/spreadsheets"),
    ("Database: SQLite", "#/sqlite"),
    ("Version Control: Git, GitHub", "#/git"),
    ("2. Deployment Tools", "#/deployment-tools"),
    ("Markdown", "#/markdown"),
    ("Images: Compression", "#/image-compression"),
    ("Static hosting: GitHub Pages", "#/github-pages"),
    ("Notebooks: Google Colab", "#/colab"),
    ("Serverless hosting: Vercel", "#/vercel"),
    ("CI/CD: GitHub Actions", "#/github-actions"),
    ("Containers: Docker, Podman", "#/docker"),
    ("DevContainers: GitHub Codespaces", "#/github-codespaces"),
    ("Tunneling: ngrok", "#/ngrok"),
    ("CORS", "#/cors"),
    ("REST APIs", "#/rest-apis"),
    ("Web Framework: FastAPI", "#/fastapi"),
    ("Authentication: Google Auth", "#/google-auth"),
    ("Local LLMs: Ollama", "#/ollama"),
    ("3. Large Language Models", "#/large-language-models"),
    ("Prompt engineering", "#/prompt-engineering"),
    ("TDS TA Instructions", "#/tds-ta-instructions"),
    ("TDS GPT Reviewer", "#/tds-gpt-reviewer"),
    ("LLM Sentiment Analysis", "#/llm-sentiment-analysis"),
    ("LLM Text Extraction", "#/llm-text-extraction"),
    ("Base 64 Encoding", "#/base64-encoding"),
    ("Vision Models", "#/vision-models"),
    ("Embeddings", "#/embeddings"),
    ("Multimodal Embeddings", "#/multimodal-embeddings"),
    ("Topic modeling", "#/topic-modeling"),
    ("Vector databases", "#/vector-databases"),
    ("RAG with the CLI)", "#/rag-cli"),
    ("Hybrid RAG with TypeSense", "#/hybrid-rag-typesense"),
    ("Function Calling", "#/function-calling"),
    ("LLM Agents", "#/llm-agents"),
    ("LLM Image Generation", "#/llm-image-generation"),
    ("LLM Speech", "#/llm-speech"),
    ("LLM Evals", "#/llm-evals"),
    ("Project 1", "#/project-tds-virtual-ta"),
    ("4. Data Sourcing", "#/data-sourcing"),
    ("Scraping with Excel", "#/scraping-with-excel"),
    ("Scraping with Google Sheets", "#/scraping-with-google-sheets"),
    ("Crawling with the CLI", "#/crawling-cli"),
    ("BBC Weather API with Python", "#/bbc-weather-api-with-python"),
    ("Scraping IMDb with JavaScript", "#/scraping-imdb-with-javascript"),
    ("Nominatim API with Python", "#/nominatim-api-with-python"),
    ("Wikipedia Data with Python", "#/wikipedia-data-with-python"),
    ("Scraping PDFs with Tabula", "#/scraping-pdfs-with-tabula"),
    ("Convert PDFs to Markdown", "#/convert-pdfs-to-markdown"),
    ("Convert HTML to Markdown", "#/convert-html-to-markdown"),
    ("LLM Website Scraping", "#/llm-website-scraping"),
    ("LLM Video Screen-Scraping", "#/llm-video-screen-scraping"),
    ("Web Automation with Playwright", "#/web-automation-with-playwright"),
    ("Scheduled Scraping with GitHub Actions", "#/scheduled-scraping-with-github-actions"),
    ("Scraping emarketer.com", "#/scraping-emarketer"),
    ("Scraping: Live Sessions", "#/scraping-live-sessions"),
    ("5. Data Preparation", "#/data-preparation"),
    ("Data Cleansing in Excel", "#/data-cleansing-in-excel"),
    ("Data Transformation in Excel", "#/data-transformation-in-excel"),
    ("Splitting Text in Excel", "#/splitting-text-in-excel"),
    ("Data Aggregation in Excel", "#/data-aggregation-in-excel"),
    ("Data Preparation in the Shell", "#/data-preparation-in-the-shell"),
    ("Data Preparation in the Editor", "#/data-preparation-in-the-editor"),
    ("Cleaning Data with OpenRefine", "#/cleaning-data-with-openrefine"),
    ("Profiling Data with Python", "#/profiling-data-with-python"),
    ("Parsing JSON", "#/parsing-json"),
    ("Data Transformation with dbt", "#/dbt"),
    ("Transforming Images", "#/transforming-images"),
    ("Extracting Audio and Transcripts", "#/extracting-audio-and-transcripts"),
    ("6. Data Analysis", "#/data-analysis"),
    ("Correlation with Excel", "#/correlation-with-excel"),
    ("Regression with Excel", "#/regression-with-excel"),
    ("Forecasting with Excel", "#/forecasting-with-excel"),
    ("Outlier Detection with Excel", "#/outlier-detection-with-excel"),
    ("Data Analysis with Python", "#/data-analysis-with-python"),
    ("Data Analysis with SQL", "#/data-analysis-with-sql"),
    ("Data Analysis with Datasette", "#/data-analysis-with-datasette"),
    ("Data Analysis with DuckDB", "#/data-analysis-with-duckdb"),
    ("Data Analysis with ChatGPT", "#/data-analysis-with-chatgpt"),
    ("Geospatial Analysis with Excel", "#/geospatial-analysis-with-excel"),
    ("Geospatial Analysis with Python", "#/geospatial-analysis-with-python"),
    ("Geospatial Analysis with QGIS", "#/geospatial-analysis-with-qgis"),
    ("Network Analysis in Python", "#/network-analysis-in-python"),
    ("Project 2", "#"),
    ("7. Data Visualization", "#/data-visualization"),
    ("Visualizing Forecasts with Excel", "#/visualizing-forecasts-with-excel"),
    ("Visualizing Animated Data with PowerPoint", "#/visualizing-animated-data-with-powerpoint"),
    ("Visualizing Animated Data with Flourish", "#/visualizing-animated-data-with-flourish"),
    ("Visualizing Network Data with Kumu", "#/visualizing-network-data-with-kumu"),
    ("Visualizing Charts with Excel", "#/visualizing-charts-with-excel"),
    ("Data Visualization with Seaborn", "#/data-visualization-with-seaborn"),
    ("Data Visualization with ChatGPT", "#/data-visualization-with-chatgpt"),
    ("Actor Network Visualization", "#/actor-network-visualization"),
    ("RAWgraphs", "#/rawgraphs"),
    ("Data Storytelling", "#/data-storytelling"),
    ("Narratives with LLMs", "#/narratives-with-llms"),
    ("Interactive Notebooks: Marimo", "#/marimo"),
]


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    for title, url in all_links:
        page.goto(BASE_URL+url, wait_until="networkidle")
        html = page.content()
        scrape(html,title)

    browser.close()

