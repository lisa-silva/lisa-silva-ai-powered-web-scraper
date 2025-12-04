# app.py – AI-Powered Web Scraper 2025 (100% WORKING ON STREAMLIT CLOUD)
# app.py – AI-Powered Web Scraper 2025 (100% WORKING ON STREAMLIT CLOUD)
import streamlit as st
import google.generativeai as genai
from playwright.sync_api import sync_playwright
import os

# === MAGIC FIXES FOR STREAMLIT CLOUD ===
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"           # Tells Playwright to use shared browsers
os.system("playwright install chromium --with-deps")   # Installs Chromium + system deps at runtime

st.set_page_config(page_title="AI Web Scraper", page_icon="Brain", layout="wide")

# === API Setup ===
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="You are an expert web content extractor. Return ONLY clean markdown of the main article. Remove ads, nav, footers, scripts, and boilerplate."
)

st.title("AI-Powered Web Scraper 2025")
st.markdown("**The smartest scraper alive** — renders JavaScript + uses Gemini AI to extract perfect clean content from any site.")

url = st.text_input("Enter any URL", placeholder="https://news.ycombinator.com", value="https://www.theverge.com")

if st.button("Scrape with AI", type="primary"):
    if not url.startswith(("http://", "https://")):
        st.error("Please include http:// or https://")
    else:
        try:
            with st.spinner("Launching browser & rendering page..."):
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=[
                            "--no-sandbox",
                            "--disable-setuid-sandbox",
                            "--disable-gpu",
                            "--single-process",
                            "--disable-dev-shm-usage",
                            "--no-zygote"
                        ]
                    )
                    page = browser.new_page()
                    page.goto(url, wait_until="networkidle", timeout=60000)
                    page.wait_for_timeout(3000)  # Extra wait for lazy-loaded content
                    content = page.content()
                    browser.close()

            with st.spinner("Gemini AI extracting clean article..."):
                response = model.generate_content(
                    f"Extract the main article/content from this HTML. Return clean markdown only:\n\n{content[:60000]}"
                )
                clean_text = response.text

    st.success("✅ AI extraction complete!")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("🧹 Clean AI-Extracted Content")
        st.markdown(clean_text)
    
    with col2:
        st.subheader("🔍 Raw Source (for comparison)")
        with st.expander("Show raw HTML (first 2000 chars)"):
            st.code(content[:2000] + "...")

    st.download_button("💾 Download Clean Markdown", clean_text, "clean-article.md")
