import streamlit as st
import feedparser
import google.generativeai as genai
import time
from datetime import datetime

# Streamlit page config
st.set_page_config(page_title="RSS News Summarizer", layout="wide")

# Initialize Gemini API
def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

# Function to fetch RSS feed
def fetch_rss_feed(url):
    try:
        feed = feedparser.parse(url)
        return feed.entries
    except Exception as e:
        st.error(f"Error fetching RSS feed: {str(e)}")
        return []

# Function to summarize text using Gemini
def summarize_article(model, article_text):
    prompt = f"""Please provide a concise 2-3 sentence summary of the following article:
    {article_text}"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Main app
def main():
    st.title("📰 RSS Feed News Summarizer")
    st.write("Get AI-powered summaries of your favorite RSS feeds using Google's Gemini")

    # Sidebar for RSS feed input
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input(
            "Enter your Gemini API Key",
            type="password",
            help="Enter your Gemini API key to use the summarization service"
        )
        
        # Pre-filled RSS sources
        prefilled_rss_sources = {
            "Slashdot": "https://rss.slashdot.org/Slashdot/slashdotMain",
            "TechCrunch": "http://feeds.feedburner.com/TechCrunch/"
        }
        
        rss_source = st.selectbox(
            "Select a pre-filled RSS source",
            options=list(prefilled_rss_sources.keys())
        )
        
        custom_rss_url = st.text_input(
            "Or enter a custom RSS Feed URL",
            help="Enter the URL of any RSS feed you want to summarize"
        )
        
        rss_url = custom_rss_url if custom_rss_url else prefilled_rss_sources[rss_source]
        
        max_articles = st.slider(
            "Maximum articles to summarize",
            min_value=1,
            max_value=20,
            value=5
        )
        
    if st.button("Fetch and Summarize"):
        # Use the API key from secrets.toml if available, otherwise use the provided API key
        api_key = api_key or st.secrets.get("GEMINI_API_KEY")
        
        if not api_key:
            st.error("Please enter your Gemini API key.")
            return
        
        try:
            model = initialize_gemini(api_key)
            
            # Show loading spinner
            with st.spinner("Fetching articles..."):
                articles = fetch_rss_feed(rss_url)
                
            if not articles:
                st.error("No articles found in the RSS feed.")
                return
            
            # Process articles
            for i, article in enumerate(articles[:max_articles]):
                if i >= max_articles:
                    break
                    
                # Create a card-like container for each article
                with st.container():
                    st.markdown("---")
                    col1, col2 = st.columns([2, 3])
                    
                    with col1:
                        st.subheader(article.title)
                        pub_date = article.get('published', 'No date available')
                        st.caption(f"Published: {pub_date}")
                        st.markdown(f"[Read original article]({article.link})")
                    
                    with col2:
                        with st.spinner("Generating summary..."):
                            # Get article content (some RSS feeds use different fields)
                            article_content = article.get('summary', article.get('description', ''))
                            summary = summarize_article(model, article_content)
                            st.markdown("### Summary")
                            st.write(summary)
                    
                    # Add some spacing
                    st.markdown("<br>", unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()