# streamlit_app.py
import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("vibetune.csv")
    return df

# Recommendation function
def recommend_by_embedding_similarity(input_text, df, top_n=10):
    total_corpus = df['corpus'].fillna('').tolist()
    total_corpus.insert(0, input_text)
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(total_corpus).toarray()
    input_vector = tfidf_matrix[0].reshape(1, -1)
    corpus_vectors = tfidf_matrix[1:]
    similarities = cosine_similarity(input_vector, corpus_vectors)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    recommendations = df.iloc[top_indices][['track_name', 'artist_name', 'spotify_url', 'image_url']].copy()
    recommendations['similarity_score'] = similarities[top_indices]
    return recommendations

# Streamlit UI
st.set_page_config(page_title="🎧 VibeTune: Music Recommender", layout="wide")

# Enhanced styling with vivid music-theme overlay and modern font
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap');

    html, body, [class*="st"]  {
        font-family: 'Raleway', sans-serif;
    }

    .stApp {
        background-image: linear-gradient(rgba(20, 20, 20, 0.7), rgba(20, 20, 20, 0.7)),
                          url('https://images.unsplash.com/photo-1485579149621-3123dd979885');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #ffffff;
    }

    .block-container {
        background: rgba(0, 0, 0, 0.65);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 0 25px rgba(0,0,0,0.6);
        max-width: 1600px;
        margin: auto;
    }

    h1, h2, h3, h4 {
        color: #ffcc70;
        text-shadow: 1px 1px 2px #000000;
    }

    label, .stTextInput > div > input {
        color: white !important;
    }

    .stButton > button {
        background-color: #789c7c;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #ffffff;
        color: black;
    }

    .stAlert > div {
        color: white;
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎧 VibeTune: Music Recommender")
st.markdown("""
Type a few words describing your **mood**, a **theme**, or even your **vibe** ✨, and get music that matches your feel.
""")

# Input
input_text = st.text_input("Describe your mood, theme, or vibe:", placeholder="e.g. heartbreak, chill vibes, summer love")

# Load dataset
df = load_data()

# Show recommendations
if st.button("🎵 Recommend Music") and input_text:
    with st.spinner("Finding your vibe... 🎶"):
        results = recommend_by_embedding_similarity(input_text, df)
        for idx, row in results.iterrows():
            st.markdown(f"**{row['track_name']}** by *{row['artist_name']}*")
            cols = st.columns([1, 4])
            with cols[0]:
                st.image(row['image_url'], width=100)
            with cols[1]:
                st.markdown(f"[▶️ Listen on Spotify]({row['spotify_url']})")
                st.progress(min(row['similarity_score'], 1.0))
else:
    st.markdown("<div class='stAlert'><p>Enter a description above and hit Recommend Songs!</p></div>", unsafe_allow_html=True)
