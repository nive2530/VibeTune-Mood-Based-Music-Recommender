# 🎧 VibeTune – Real-Time Mood-Based Music Recommendation Engine

**VibeTune** is a real-time, content-aware music recommendation system that analyzes listener mood inputs and maps them to relevant tracks using a modern cloud-native data pipeline. It is designed to handle large-scale audio metadata using distributed processing, scalable storage, and semantic vector-based recommendation techniques.

---

## 🔧 Tech Stack

| Layer               | Tools/Tech                                    |
|--------------------|-----------------------------------------------|
| **Streaming**      | AWS MSK Kafka                                 |
| **Storage**        | Amazon S3 (Staging + Data Lake)               |
| **ETL**            | AWS Glue (PySpark), AWS Glue Crawlers         |
| **Query Engine**   | Amazon Athena, Amazon Redshift                |
| **ML/Similarity**  | TF-IDF Vectorizer, Cosine Similarity (Sklearn) |
| **Frontend**       | Streamlit (Python, Custom CSS)                |

---

## 🛠️ Key Features

- **Real-Time Ingestion:**
  - Ingests four Spotify dataset components: `tracks`, `artists`, `features`, and `albums`.
  - Utilizes **AWS MSK (Kafka)** to stream data from producers to consumers in near real-time.

- **Scalable ETL & Data Lake:**
  - Kafka-streamed files are staged into **Amazon S3**.
  - Transformation, normalization, and merging are handled via **PySpark-based Glue ETL Jobs**.
  - Data is persisted into a centralized, partitioned **S3 data lake**.
  - **AWS Glue Crawlers** infer schema for analytical querying.

- **Analytics & Querying:**
  - Transformed data is accessible via **Amazon Athena** or **Redshift** for downstream use.
  - Enables SQL-based exploration and dashboard integration.

- **Content-Based Recommendation Engine:**
  - Combines Spotify metadata fields (e.g., genre, tags, mood) with lyrics and descriptions.
  - Creates a **corpus** of track-tag + lyric text.
  - Applies **TF-IDF vectorization** to build track embeddings.
  - Computes **cosine similarity** between user input and existing vectors.

- **Frontend - Streamlit Web App:**
  - Responsive and immersive **Streamlit interface**.
  - Accepts mood/theme inputs like: _"chill sad acoustic"_ or _"summer roadtrip pop"_.
  - Renders top 10 recommended songs with:
    - 🎵 Track Name
    - 🎤 Artist
    - 🖼️ Album Art
    - 🔗 Direct Spotify link
    - 📊 Similarity Score Indicator

---

## 💡 How It Works

```text
+----------------------+              +------------------------+
|   User Input (Text)  |  ---> TF-IDF|   Input Vector         |
+----------------------+              +------------------------+
                                                 |
                                                 v
                              +----------------------------+
                              | Cosine Similarity Matching |
                              +----------------------------+
                                                 |
                                                 v
                    +------------------------------------------+
                    | Top 10 Closest Track Vectors (Results)   |
                    +------------------------------------------+
                                                 |
                                                 v
                          +-------------------------------+
                          | Streamlit UI (Display Output) |
                          +-------------------------------+
```

---

## 📂 Repository Structure

```
VibeTune-Mood-Based-Music-Recommender/
├── Dataset/                        # (Large files hosted externally)
├── etl_jobs/                      # PySpark Glue job scripts
├── notebooks/                     # EDA, Vectorization, Similarity Calculation
├── streamlit_app.py               # Streamlit app UI & logic
├── utils/                         # Preprocessing or NLP utilities
├── mood_tagged_tracks.csv         # Final processed CSV with mood labels
├── mood_model.pkl                 # TF-IDF model for input similarity
├── requirements.txt               # Python dependencies
└── README.md                      # You are here 🚀
```

---

## 📎 Dataset

The Spotify dataset used is a collection of metadata from **Kaggle: Spotify Dataset 2023** including track-level, album-level, and artist-level information.

Due to GitHub file limits, you can access the full dataset here:

📊 [[Kaggle – Spotify Dataset 2023](https://www.kaggle.com/datasets/](https://www.kaggle.com/datasets/tonygordonjr/spotify-dataset-2023))

---

## 🚀 Future Enhancements
- 🎯 Integrate Spotify API for real-time search & playback.
- 🧠 Switch to semantic embeddings (e.g., Sentence-BERT) for better recommendations.
- 🗺️ Cluster-based mood analysis (e.g., k-means, PCA on audio features).
- 📱 Deploy as a PWA/mobile app for daily mood playlists.
