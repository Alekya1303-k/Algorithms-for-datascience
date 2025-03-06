import requests
import pandas as pd
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

class URLValidator:
    def __init__(self):
        self.similarity_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.fake_news_classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")
        self.sentiment_analyzer = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")

    def fetch_page_content(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return " ".join([p.text for p in soup.find_all("p")])
        except requests.RequestException:
            return ""

    def compute_similarity_score(self, user_query: str, content: str) -> int:
        if not content:
            return 0
        return int(util.pytorch_cos_sim(self.similarity_model.encode(user_query), self.similarity_model.encode(content)).item() * 100)

    def detect_fake_news(self, content: str) -> int:
        if not content:
            return 50
        result = self.fake_news_classifier(content[:512])[0]
        return 100 if result["label"] == "REAL" else 30

    def detect_bias(self, content: str) -> int:
        if not content:
            return 50
        sentiment_result = self.sentiment_analyzer(content[:512])[0]
        return 100 if sentiment_result["label"] == "POSITIVE" else 50 if sentiment_result["label"] == "NEUTRAL" else 30

    def get_star_rating(self, score: float) -> tuple:
        stars = max(1, min(5, round(score / 20)))
        return stars, "⭐" * stars

    def rate_url_validity(self, user_query: str, url: str, func_rating: int, custom_rating: int) -> dict:
        content = self.fetch_page_content(url)
        similarity_score = self.compute_similarity_score(user_query, content)
        fake_news_score = self.detect_fake_news(content)
        bias_score = self.detect_bias(content)

        final_score = (0.4 * similarity_score) + (0.3 * fake_news_score) + (0.3 * bias_score)
        stars, icon = self.get_star_rating(final_score)

        return {
            "user_prompt": user_query,
            "url_to_check": url,
            "scores": {
                "Content Relevance": similarity_score,
                "Fake News Detection": fake_news_score,
                "Bias Score": bias_score,
                "Final Score": final_score
            },
            "ratings": {
                "func_rating": func_rating,
                "custom_rating": custom_rating
            },
            "stars": {
                "score": stars,
                "icon": icon
            }
        }

# Load CSV and process multiple entries
def process_csv(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)
    validator = URLValidator()
    results = []
    
    for _, row in df.iterrows():
        result = validator.rate_url_validity(row["user_prompt"], row["url_to_check"], row["func_rating"], row["custom_rating"])
        results.append(result)
    
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)

# Example usage
# process_csv("input.csv", "output.csv")
