# ==============================================
# Spotify Trend Modeling – R^2 for Genre & Artist + 8 vars
# Deps: pandas, statsmodels
# ==============================================
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

CSV_PATH = "data_with_songscore.csv"  # đổi nếu cần

# ----- Load data -----
df = pd.read_csv(CSV_PATH)

# ----- Chọn biến mục tiêu -----
y_col = "SongScore" if "SongScore" in df.columns else ("Popularity" if "Popularity" in df.columns else None)
if y_col is None:
    raise ValueError("Không tìm thấy cột mục tiêu SongScore/Popularity trong CSV.")

# ====== (A) REGRESSION: chỉ với Artist + Genre ======
# Giữ cột cần thiết
need_cols = [y_col, "Artist", "MainGenre"]
need_cols = [c for c in need_cols if c in df.columns]
dfa = df[need_cols].dropna()

# Lọc nghệ sĩ có >=3 bài (giúp hệ số ổn định hơn)
if "Artist" in dfa.columns:
    valid_artists = dfa["Artist"].value_counts()
    keep_artists = valid_artists[valid_artists >= 3].index
    dfa = dfa[dfa["Artist"].isin(keep_artists)]

# Nếu thiếu Artist/Genre thì dừng phần A
if not set(["Artist","MainGenre"]).issubset(dfa.columns):
    print("⚠️ Thiếu Artist/MainGenre nên bỏ qua phần (A) hồi quy theo Artist+Genre.")
else:
    # Dùng công thức C() để tự one-hot (tránh bẫy giả, drop_first)
    formula_a = f"{y_col} ~ C(Artist) + C(MainGenre)"
    model_a = smf.ols(formula=formula_a, data=dfa).fit(cov_type="HC3")
    print("\n===== (A) OLS: Artist + Genre =====")
    print(f"R²      : {model_a.rsquared:.4f}  ({model_a.rsquared*100:.2f}%)")
    print(f"Adj.R²  : {model_a.rsquared_adj:.4f}")
    print(model_a.summary().tables[0])  # Bảng tóm tắt nhỏ gọn (head)
    # Nếu cần full summary: print(model_a.summary())

# ====== (B) REGRESSION: 8 biến bạn liệt kê ======
# Chuẩn hóa tên cột để khớp dữ liệu thực
candidate_cols = [
    "log_Total_norm",
    "Unique_norm",
    "Recency_norm",
    "Year",
    "log_Total",
    "Stream_x_Recency",
    "Genre_Pop",
    "Genre_HipHop_Rap",      # phiên bản không dấu gạch chéo
    "Genre_Hip-Hop / Rap"    # phiên bản có " / "
]

# Lấy các cột thật sự có trong file
present = [c for c in candidate_cols if c in df.columns]
if "Genre_Hip-Hop / Rap" in present and "Genre_HipHop_Rap" in present:
    # Tránh trùng lặp khi cùng ý nghĩa
    present.remove("Genre_Hip-Hop / Rap")

if len(present) == 0:
    print("\n⚠️ Không tìm thấy cột nào trong 8 biến bạn yêu cầu. Bỏ qua phần (B).")
else:
    cols_b = [y_col] + present
    dfb = df[cols_b].dropna()
    y = dfb[y_col]
    X = dfb.drop(columns=[y_col])

    # Thêm hằng số
    X = sm.add_constant(X, has_constant="add")

    model_b = sm.OLS(y, X).fit(cov_type="HC3")
    print("\n===== (B) OLS: 8 biến theo yêu cầu =====")
    print(f"Sử dụng các biến: {list(X.columns)}")
    print(f"R²      : {model_b.rsquared:.4f}  ({model_b.rsquared*100:.2f}%)")
    print(f"Adj.R²  : {model_b.rsquared_adj:.4f}")
    # In top hệ số theo độ lớn (trừ const)
    coefs = model_b.params.drop(labels=["const"]) if "const" in model_b.params.index else model_b.params
    coefs = coefs.reindex(coefs.abs().sort_values(ascending=False).index)
    print("\nTop hệ số (|β| lớn nhất):")
    for k, v in coefs.head(10).items():
        print(f"  {k:20s}: {v:+.4f}")
