from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launch a persistent browser with its own user data directory
    context = p.chromium.launch_persistent_context(
        user_data_dir="auth_profile",
        headless=False  # visible for manual login
    )

    page = context.new_page()
    page.goto("https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34")  # This will redirect to Google OAuth

    # WAIT: Manually complete the login in the browser window.
    input("After login is complete and you see the dashboard, press Enter here...")

    # Save login state
    context.storage_state(path="auth.json")
    context.close()
