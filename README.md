# Song Recommendation System using Spotify Data 
A data-driven **Song Recommendation System** that predicts and recommends similar tracks based on audio features, genre, and popularity — powered by **Python, SQL, and Machine Learning**.

# Tech stack 
|category| Tools / Libraries|
|--------|-----------------|
|** DATA SOUCES ** | Spotify API, Selenium, MusicBrainAPI|
|** DATA BASE ** | SQL Sever (via pydbc)|
|** VISUALIZE **| Matplotlib\ SearnBorn|
## 🧱 3. Data Pipeline

```mermaid
graph TD
A[Web Crawling / API] --> B[Data Cleaning]
B --> C[SQL Storage]
C --> D[Feature Engineering]
D --> E[Model Training]
E --> F[Recommendation Output]
