import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Lớp cha: Dùng chung cho tất cả biểu đồ
class BasePlot:
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath)

    def info(self):
        print(self.data.info())
        print(self.data.head())


# MATPLOTLIB (5 biểu đồ)

#  Bar chart – Top 10 Nghệ sĩ
class ArtistBarChart_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 5))
        top_artists = self.data["Artist"].value_counts().head(10)
        plt.bar(top_artists.index, top_artists.values, color='lightblue', edgecolor='black')
        plt.title(" Top 10 Nghệ sĩ (Matplotlib)")
        plt.xlabel("Artist")
        plt.ylabel("Số lượng bài hát")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


#  Histogram – Phân bố độ phổ biến
class PopularityHistogram_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        plt.hist(self.data["Popularity"], bins=20, color='orange', edgecolor='black')
        plt.title(" Phân bố độ phổ biến (Matplotlib)")
        plt.xlabel("Popularity")
        plt.ylabel("Số lượng bài hát")
        plt.tight_layout()
        plt.show()


#  Scatter – Pkstreams vs Popularity
class ScatterPkstreams_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        plt.scatter(self.data["Pkstreams"], self.data["Popularity"], alpha=0.6, c='red')
        plt.title(" Pkstreams vs Popularity (Matplotlib)")
        plt.xlabel("Pkstreams")
        plt.ylabel("Popularity")
        plt.tight_layout()
        plt.show()


#  Line chart – Xu hướng theo Wks
class LineWks_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        wks_avg = self.data.groupby("Wks")["Popularity"].mean()
        plt.plot(wks_avg.index, wks_avg.values, marker='o', color='green')
        plt.title(" Xu hướng Popularity theo Wks (Matplotlib)")
        plt.xlabel("Wks")
        plt.ylabel("Popularity trung bình")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


#  Heatmap – Ma trận tương quan
class Heatmap_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 8))
        corr = self.data.select_dtypes(include='number').corr()
        plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
        plt.colorbar(label="Hệ số tương quan")
        plt.xticks(range(len(corr)), corr.columns, rotation=45, ha='right')
        plt.yticks(range(len(corr)), corr.columns)
        plt.title(" Ma trận tương quan (Matplotlib)")
        plt.tight_layout()
        plt.show()


# SEABORN (5 biểu đồ)

#  Barplot – Nghệ sĩ phổ biến (Top 10)
class ArtistBarChart_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 5))
        top_artists = self.data["Artist"].value_counts().head(10).index
        sns.barplot(data=self.data[self.data["Artist"].isin(top_artists)],
                    x="Artist", y="Popularity", errorbar=None, palette="Blues_r")
        plt.title(" Top 10 Nghệ sĩ có độ phổ biến cao nhất (Seaborn)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


#  Histogram – Phân bố Popularity
class PopularityHistogram_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        sns.histplot(self.data["Popularity"], bins=20, kde=True, color="skyblue")
        plt.title(" Phân bố độ phổ biến bài hát (Seaborn)")
        plt.xlabel("Popularity")
        plt.ylabel("Số lượng bài hát")
        plt.tight_layout()
        plt.show()


#  Boxplot – So sánh độ phổ biến theo thể loại
class GenreBoxPlot_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 6))
        top_genres = self.data["Genre"].value_counts().head(5).index
        sns.boxplot(data=self.data[self.data["Genre"].isin(top_genres)],
                    x="Genre", y="Popularity", palette="Set3")
        plt.title(" So sánh độ phổ biến theo thể loại (Seaborn)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


#  Scatterplot – Pkstreams vs Popularity
class ScatterPkstreams_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=self.data, x="Pkstreams", y="Popularity", hue="Genre", alpha=0.7)
        plt.title(" Mối quan hệ giữa Pkstreams và Popularity (Seaborn)")
        plt.tight_layout()
        plt.show()


#  Heatmap – Ma trận tương quan
class Heatmap_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 8))
        corr = self.data.select_dtypes("number").corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(" Ma trận tương quan giữa các thuộc tính số (Seaborn)")
        plt.tight_layout()
        plt.show()


def main():
    path = "data lab.csv"

    # --- Matplotlib ---
    mpl1 = ArtistBarChart_MPL(path)
    mpl2 = PopularityHistogram_MPL(path)
    mpl3 = ScatterPkstreams_MPL(path)
    mpl4 = LineWks_MPL(path)
    mpl5 = Heatmap_MPL(path)

    # --- Seaborn ---
    sns1 = ArtistBarChart_SNS(path)
    sns2 = PopularityHistogram_SNS(path)
    sns3 = GenreBoxPlot_SNS(path)
    sns4 = ScatterPkstreams_SNS(path)
    sns5 = Heatmap_SNS(path)

    # chạy test 
    sns5.draw()



if __name__ == "__main__":
    main()
