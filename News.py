import streamlit as st
from GoogleNews import GoogleNews
from transformers import pipeline
import pandas as pd

# Function to fetch stock market and business news data
def fetch_news(keyword, start, count=10):
    googlenews = GoogleNews(lang='en', region='US')
    googlenews.search(keyword)
    googlenews.getpage(1)  # Ensure the first page is fetched
    news_results = googlenews.results()

    for page in range(2, 6):
        googlenews.getpage(page)
        news_results.extend(googlenews.results())

    return news_results[start:start+count]

# AI Sentiment Analysis function
def analyze_sentiment(news_articles):
    # Load sentiment analysis pipeline from Hugging Face
    sentiment_analyzer = pipeline("sentiment-analysis")

    # Analyze sentiment for each article
    sentiment_results = []
    for article in news_articles:
        sentiment = sentiment_analyzer(article['desc'])[0]
        sentiment_results.append((article, sentiment['label'], sentiment['score']))
    
    return sentiment_results

# Streamlit UI
def main():
    st.set_page_config(page_title="Stock Investor News", page_icon="💹", layout="wide")

    # Title with professional styling
    st.markdown(
        """
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; text-align: center;">
            <h1 style="color: #000000;">💹 Stock Investor News 💹</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 📰 Get the Latest Stock Market & Business News")

    topics = ['Stock Market', 'Investing', 'Economy', 'Business', 'Finance', 'Cryptocurrency', 'IPO', 'Trading']
    selected_topic = st.selectbox("Select a topic", topics)

    if 'news_start' not in st.session_state:
        st.session_state.news_start = 0
    if 'news_data' not in st.session_state:
        st.session_state.news_data = []

    if st.button("🔍 Fetch News"):
        st.session_state.news_start = 0
        st.session_state.news_data = fetch_news(selected_topic, st.session_state.news_start)
        st.session_state.news_start += 10

    # Display news with AI-powered insights
    if st.session_state.news_data:
        sentiment_results = analyze_sentiment(st.session_state.news_data)
        df = pd.DataFrame(sentiment_results, columns=["Article", "Sentiment", "Score"])

        for index, row in df.iterrows():
            article = row['Article']
            sentiment = row['Sentiment']
            score = row['Score']
            sentiment_text = f"Sentiment: {sentiment} (Confidence: {score:.2f})"

            # Display the article with sentiment information
            st.markdown(
                f"""
                <div style="background-color: #e0e0e0; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h2 style="color: #000000;">{index+1}. {article['title']}</h2>
                    <p style="color: #555555;"><strong>Source:</strong> {article['media']} | <strong>Published on:</strong> {article['date']}</p>
                    <p style="color: #000000; font-size: 16px;"><strong>Summary:</strong> {sentiment_text}</p>
                    <p style="color: #000000; font-size: 16px;">{article['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("📥 Load More"):
            additional_news = fetch_news(selected_topic, st.session_state.news_start)
            if additional_news:
                st.session_state.news_data.extend(additional_news)
                st.session_state.news_start += 10
                sentiment_results = analyze_sentiment(additional_news)
                additional_df = pd.DataFrame(sentiment_results, columns=["Article", "Sentiment", "Score"])

                for index, row in additional_df.iterrows():
                    article = row['Article']
                    sentiment = row['Sentiment']
                    score = row['Score']
                    sentiment_text = f"Sentiment: {sentiment} (Confidence: {score:.2f})"

                    st.markdown(
                        f"""
                        <div style="background-color: #e0e0e0; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                            <h2 style="color: #000000;">{len(df) + index + 1}. {article['title']}</h2>
                            <p style="color: #555555;"><strong>Source:</strong> {article['media']} | <strong>Published on:</strong> {article['date']}</p>
                            <p style="color: #000000; font-size: 16px;"><strong>Summary:</strong> {sentiment_text}</p>
                            <p style="color: #000000; font-size: 16px;">{article['desc']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.rerun()
            else:
                st.info("No more news articles available.")

if __name__ == "__main__":
    main()
