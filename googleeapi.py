# streamlit_app.py
import streamlit as st
from gnews import GNews
from datetime import datetime, timedelta
import pandas as pd

# Page config
st.set_page_config(page_title="Company News Dashboard", layout="wide")

# Title
st.title("📰 Company News Dashboard (Google News API)")
st.write("Fetch and explore recent news about companies such as Dabur India Ltd.")

# Sidebar input
company = st.sidebar.text_input("Enter Company Name", "Dabur India Ltd")

# Initialize GNews client
google_news = GNews(language='en', country='IN', max_results=50)

# Function to fetch and filter news
def get_news(company, days_back):
    news = google_news.get_news(company)
    df = pd.DataFrame(news)
    if df.empty:
        return pd.DataFrame(columns=["title", "published date", "url", "publisher"])
    df["published date"] = pd.to_datetime(df["published date"])
    cutoff_date = datetime.now() - timedelta(days=days_back)
    return df[df["published date"] >= cutoff_date]

# Time frames
timeframes = {
    "🗞️ Last Week": 7,
    "📅 Last Month": 30,
    "🧭 Last 3 Months": 90
}

# Layout
for label, days in timeframes.items():
    st.subheader(label)
    df = get_news(company, days)
    if df.empty:
        st.info(f"No news found for {company} in {label.lower()}.")
    else:
        for _, row in df.iterrows():
            with st.expander(row["title"]):
                st.write(f"**Source:** {row['publisher']['title'] if isinstance(row['publisher'], dict) else row['publisher']}")
                st.write(f"**Published:** {row['published date'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"[Read more →]({row['url']})")

st.markdown("---")
st.caption("Powered by Google News via GNews Python API • Streamlit App")
