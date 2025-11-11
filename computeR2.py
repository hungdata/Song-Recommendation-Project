import pandas as pd
import statsmodels.formula.api as smf

# --- 1. Đọc dữ liệu ---
df = pd.read_csv(r"C:\Users\trung\OneDrive\Máy tính\MusicChart\Base.csv")

df.columns = df.columns.str.lower()

# --- 2. Kiểm tra & làm sạch ---
df = df.dropna(subset=["songscore", "artist", "genre"])
df = df[df["artist"].astype(str).str.strip() != ""]
df = df[df["genre"].astype(str).str.strip() != ""]

# --- 3. Mô hình hồi quy: SongScore ~ Artist + Genre ---
model = smf.ols("songscore ~ C(artist) + C(genre)", data=df).fit()

# --- 4. In kết quả ---
print("===== KẾT QUẢ HỒI QUY =====")
print(f"Số bài hát: {len(df)}")
print(f"Số nghệ sĩ: {df['artist'].nunique()}")
print(f"Số thể loại: {df['genre'].nunique()}")
print("----------------------------------")
print(f"R² = {model.rsquared:.4f} → {model.rsquared*100:.2f}%")
print(f"Adjusted R² = {model.rsquared_adj:.4f}")
print("----------------------------------")

# (tuỳ chọn) In bảng hệ số quan trọng nhất
print("\nTop 10 biến có ảnh hưởng mạnh nhất:")
print(model.summary2().tables[1].sort_values("Coef.", ascending=False).head(10))
