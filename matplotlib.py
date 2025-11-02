import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv(r"C:\Users\DELL\Downloads\spotify_tracks_export (1).csv")

# 1️⃣ Biểu đồ cột: Top 10 Nghệ sĩ
plt.figure(figsize=(10, 5))
top_artists = data["Artist"].value_counts().head(10)
plt.bar(top_artists.index, top_artists.values)
plt.title("Top 10 Nghệ sĩ")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 2️⃣ Histogram: Phân bố Popularity
plt.figure(figsize=(8, 5))
plt.hist(data["Popularity"], bins=20, edgecolor='black')
plt.title("Phân bố độ phổ biến")
plt.xlabel("Popularity")
plt.ylabel("Số lượng")
plt.show()

# 4️⃣ Scatter: Pkstreams vs Popularity
plt.figure(figsize=(8, 5))
plt.scatter(data["Pkstreams"], data["Popularity"], alpha=0.5)
plt.xlabel("Pkstreams")
plt.ylabel("Popularity")
plt.title("Pkstreams vs Popularity")
plt.show()

# 5️⃣ Line: Xu hướng theo Wks
plt.figure(figsize=(8, 5))
wks_avg = data.groupby("Wks")["Popularity"].mean()
plt.plot(wks_avg.index, wks_avg.values, marker='o')
plt.xlabel("Wks")
plt.ylabel("Popularity")
plt.title("Xu hướng Popularity theo Wks")
plt.grid(True, alpha=0.3)
plt.show()

# 6️⃣ Heatmap: Tương quan
plt.figure(figsize=(10, 8))
corr = data.select_dtypes(include='number').corr()
plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns, rotation=45, ha='right')
plt.yticks(range(len(corr)), corr.columns)
plt.title("Ma trận tương quan")
plt.tight_layout()
plt.show()