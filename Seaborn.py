
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv(r"C:\Users\DELL\Downloads\spotify_tracks_export (1).csv")
data.head()

# 1️⃣ Biểu đồ cột: Độ phổ biến theo Nghệ sĩ (Top 10)
plt.figure(figsize=(10, 5))
top_artists = data["Artist"].value_counts().head(10).index
sns.barplot(data=data[data["Artist"].isin(top_artists)],
            x="Artist", y="Popularity", errorbar=None)
plt.title("Top 10 Nghệ sĩ có độ phổ biến cao nhất")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2️⃣ Histogram: Phân bố độ phổ biến
plt.figure(figsize=(8, 5))
sns.histplot(data["Popularity"], bins=20, kde=True)
plt.title("Phân bố độ phổ biến bài hát")
plt.xlabel("Popularity")
plt.ylabel("Số lượng bài hát")
plt.show()

# 3️⃣ Boxplot: So sánh độ phổ biến theo Thể loại
plt.figure(figsize=(10, 6))
top_genres = data["Genre"].value_counts().head(5).index
sns.boxplot(data=data[data["Genre"].isin(top_genres)],
            x="Genre", y="Popularity")
plt.title("So sánh độ phổ biến giữa các thể loại (Top 5 Genre)")
plt.xticks(rotation=45)
plt.show()


# 4️⃣ Scatterplot: Mối quan hệ giữa Pkstreams và Popularity
plt.figure(figsize=(8, 5))
sns.scatterplot(data=data, x="Pkstreams", y="Popularity", hue="Genre", alpha=0.7)
plt.title("Mối quan hệ giữa Pkstreams và Popularity")
plt.show()


# 5️⃣ Lineplot: Xu hướng Popularity theo số tuần (Wks)
plt.figure(figsize=(8, 5))
sns.lineplot(data=data, x="Wks", y="Popularity")
plt.title("Xu hướng độ phổ biến theo số tuần xuất hiện (Wks)")
plt.show()


# 6️⃣ Heatmap: Ma trận tương quan giữa các cột số
plt.figure(figsize=(10, 8))
num_cols = data.select_dtypes("number")
corr = num_cols.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Ma trận tương quan giữa các thuộc tính số")
plt.show()
