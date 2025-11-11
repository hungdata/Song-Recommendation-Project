import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import r2_score, mean_squared_error
from scipy.stats import f_oneway
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Load dữ liệu
# -----------------------------
df = pd.read_csv("merged_music_dataset_fully_filled.csv")

columns_needed = ['artist','genre','tempo','danceability','energy','valence',
                  'acousticness','loudness','speechiness','duration_ms','songscore']
df = df[columns_needed]
df = df.dropna(subset=['songscore'])
num_cols = ['tempo','danceability','energy','valence','acousticness',
            'loudness','speechiness','duration_ms']

# Fill numeric missing
for col in num_cols:
    df[col] = df[col].fillna(df[col].min())

df['artist'] = df['artist'].str.lower()
df['genre'] = df['genre'].str.lower()

# -----------------------------
# Chuẩn hóa songscore 0→100
# -----------------------------
min_score = df['songscore'].min()
max_score = df['songscore'].max()
df['songscore'] = (df['songscore'] - min_score) / (max_score - min_score) * 100

# -----------------------------
# Artist target encoding
# -----------------------------
artist_means = df.groupby('artist')['songscore'].mean().to_dict()
artist_min = df['songscore'].min()
df['artist_enc'] = df['artist'].map(artist_means).fillna(artist_min)

# -----------------------------
# Genre → Multi-hot encoding (tất cả genre trước ANOVA)
# -----------------------------
all_genres = df['genre'].str.split(',').explode().str.strip().unique().tolist()

def filter_genre(text):
    genres = [g.strip() for g in text.split(',')]
    return ','.join([g for g in genres if g in all_genres])

df['genre_filtered'] = df['genre'].apply(filter_genre)

vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','), lowercase=True)
genre_matrix = vectorizer.fit_transform(df['genre_filtered'])
genre_df = pd.DataFrame(genre_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# -----------------------------
# ANOVA test để chọn genre quan trọng
# -----------------------------
anova_results = []
for genre in genre_df.columns:
    group_yes = df['songscore'][genre_df[genre] == 1]
    group_no  = df['songscore'][genre_df[genre] == 0]
    f, p = f_oneway(group_yes, group_no)
    anova_results.append({'genre': genre, 'F': f, 'p': p})

anova_df = pd.DataFrame(anova_results)
anova_df = anova_df.sort_values('F', ascending=False)

# Chọn genre significant
significant_genres = anova_df[anova_df['p'] < 0.05]

# Top 20 genres
top_genres = significant_genres.head(20)['genre'].tolist()
print("Top 20 genres sau ANOVA:", top_genres)

# Vẽ biểu đồ trực quan
plt.figure(figsize=(10,6))
sns.barplot(x='F', y='genre', data=significant_genres.head(20), palette='viridis')
plt.title('Top 20 genres ảnh hưởng nhất đến songscore')
plt.xlabel('F-value')
plt.ylabel('Genre')
plt.show()

genre_df_selected = genre_df[top_genres] * 0.3  # giảm tác động

# -----------------------------
#  Chuẩn hóa numeric
# -----------------------------
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# -----------------------------
#  Tạo X, y và heatmap lọc thêm
# -----------------------------
X = pd.concat([df[num_cols], df[['artist_enc']], genre_df_selected], axis=1)
y = df['songscore']

df_corr = pd.concat([X, y], axis=1)
corr_matrix = df_corr.corr()

plt.figure(figsize=(15, 13))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
            cbar=True, square=False, linewidths=0.5,
            annot_kws={"size": 6})
plt.xticks(rotation=80, fontsize=8) 
plt.yticks(rotation=0, fontsize=8)   

plt.title("Heatmap correlation with songscore", fontsize=15)
plt.tight_layout()
plt.show()

# Chọn feature theo correlation tuyệt đối >=0.01
feature_corr = corr_matrix['songscore'].drop('songscore').abs().sort_values(ascending=False)
selected_features = feature_corr[feature_corr >= 0.01].index.tolist()
print("Feature được chọn để train:", selected_features)

X_selected = X[selected_features]

# -----------------------------
#  Train/test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# -----------------------------
# Train CatBoost
# -----------------------------
model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=8,
    verbose=100,
    random_seed=42
)
model.fit(X_train, y_train)

# -----------------------------
#  Đánh giá model
# -----------------------------
y_pred = model.predict(X_test)
print("R²:", round(r2_score(y_test, y_pred), 4))
print("RMSE:", round(mean_squared_error(y_test, y_pred, squared=False), 4))

# -----------------------------
#  Nhập bài hát mới
# -----------------------------
def input_new_song():
    new_song = {}
    for col in ['artist','genre'] + num_cols:
        val = input(f"Nhập giá trị cho {col}: ").strip()
        if col in num_cols:
            try:
                val = float(val)
            except:
                val = df[col].min()
        else:
            val = val.lower() if val else ""
        new_song[col] = val
    return new_song

new_song_raw = input_new_song()

# -----------------------------
#  Xử lý giống train
# -----------------------------
artist_enc = artist_means.get(new_song_raw['artist'], artist_min)

genres_filtered = [g.strip() for g in new_song_raw['genre'].split(',') if g.strip() in top_genres]
genre_text = ','.join(genres_filtered)
new_genre_vec = vectorizer.transform([genre_text])
genre_df_new = pd.DataFrame(new_genre_vec.toarray(), columns=vectorizer.get_feature_names_out())
genre_df_new = genre_df_new[top_genres] * 0.3

num_vals = [new_song_raw[col] if isinstance(new_song_raw[col], float) else df[col].min() for col in num_cols]
num_vals = scaler.transform([num_vals])[0]

X_new = pd.DataFrame([num_vals], columns=num_cols)
X_new['artist_enc'] = artist_enc
X_new = pd.concat([X_new.reset_index(drop=True), genre_df_new.reset_index(drop=True)], axis=1)

for col in X_selected.columns:
    if col not in X_new.columns:
        X_new[col] = 0
X_new = X_new[X_selected.columns]

# -----------------------------
# Predict song score mới
# -----------------------------
predicted_score = model.predict(X_new)[0]
print("🎵 Song score ước lượng:", round(predicted_score, 2))
