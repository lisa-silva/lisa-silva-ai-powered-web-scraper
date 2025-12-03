import streamlit as st
import google.generativeai as genai
from playwright.sync_api import sync_playwright
import time

st.set_page_config(page_title="AI Web Scraper", page_icon="🧠", layout="wide")

# === Secrets ===
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="You are an expert web content extractor. Return ONLY the main article text in clean markdown. Remove navigation, ads, footers, comments, and boilerplate. Keep headings, lists, and paragraphs intact."
)

st.title("🧠 AI-Powered Web Scraper")
st.markdown("**The smartest scraper in 2025** — uses real browser + Gemini AI to extract perfect clean content from any site (even heavy JavaScript ones).")

url = st.text_input("Enter any URL", placeholder="https://news.ycombinator.com", value="https://www.theverge.com/2025")

if st.button("🚀 Scrape with AI", type="primary"):
    if not url.startswith("http"):
        st.error("Include http:// or https://")
        st.stop()

    with st.spinner("Launching browser & rendering page..."):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            time.sleep(2)
            content = page.content()
            browser.close()

    with st.spinner("Gemini AI is extracting clean article..."):
        response = model.generate_content(
            f"Extract the main article/content from this HTML. Return clean markdown:\n\n{content[:30000]}"
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