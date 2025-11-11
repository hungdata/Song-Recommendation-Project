import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu
df = pd.read_csv("merged_music_dataset_fully_filled.csv")
df.columns = df.columns.str.lower()

# Tính trung bình SongScore theo nghệ sĩ
artist_avg = df.groupby("artist")["songscore"].mean().sort_values(ascending=False).head(10)

# Vẽ biểu đồ
plt.figure(figsize=(10,6))
artist_avg.plot(kind="bar", color="steelblue")
plt.title("Ảnh hưởng của Nghệ sĩ đến SongScore (Top 10)", fontsize=14)
plt.xlabel("Nghệ sĩ")
plt.ylabel("SongScore trung bình")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
# Trung bình SongScore theo thể loại
genre_avg = df.groupby("genre")["songscore"].mean().sort_values(ascending=False)

# Vẽ biểu đồ


# dò tên cột mục tiêu & genre
target = "songscore" if "songscore" in df.columns else ("popularity" if "popularity" in df.columns else None)
genre_col = "genre" if "genre" in df.columns else ("maingenre" if "maingenre" in df.columns else None)

if target is None:
    raise KeyError("Không tìm thấy cột 'songscore' hoặc 'popularity' trong CSV.")
if genre_col is None:
    raise KeyError("Không tìm thấy cột 'genre' hoặc 'maingenre' trong CSV.")

# ép kiểu số cho target (tránh 'no numeric data to plot')
df[target] = pd.to_numeric(df[target], errors="coerce")

# lọc sạch
dff = df[[genre_col, target]].dropna()
dff = dff[dff[genre_col].astype(str).str.strip() != ""]

# group & lấy top N
TOP_N_GENRES = 10
genre_avg = (
    dff.groupby(genre_col, dropna=False)[target]
       .mean()
       .sort_values(ascending=False)
       .head(TOP_N_GENRES)
)

# nếu rỗng, báo rõ để bạn biết
if genre_avg.empty:
    raise ValueError(
        f"Không có dữ liệu hợp lệ để vẽ. Kiểm tra lại cột '{genre_col}' và '{target}'. "
        f"Các cột hiện có: {list(df.columns)}"
    )

# ==== VẼ HÌNH 2 ====
plt.figure(figsize=(10, 6))
bars = plt.bar(genre_avg.index.astype(str), genre_avg.values)

plt.title("Ảnh hưởng của Thể loại đến " + target.capitalize() + f" (Top {TOP_N_GENRES})", fontsize=14, weight="bold")
plt.xlabel("Thể loại", fontsize=12)
plt.ylabel(f"{target.capitalize()} trung bình", fontsize=12)
plt.xticks(rotation=45, ha="right")

# gắn nhãn số trên cột
for b in bars:
    y = b.get_height()
    plt.text(b.get_x() + b.get_width()/2, y, f"{y:.2f}", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.show()
