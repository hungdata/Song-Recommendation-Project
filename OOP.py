import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod   # ✨ Import lớp trừu tượng


# 🔶 Lớp cha trừu tượng
class BasePlot(ABC):
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath)

    def info(self):
        print(self.data.info())
        print(self.data.head())

    @abstractmethod
    def draw(self):
        """Phương thức trừu tượng: lớp con phải override"""
        pass


# ---------------------- MATPLOTLIB ----------------------

class ArtistBarChart_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 5))
        top_artists = self.data["Artist"].value_counts().head(10)
        plt.bar(top_artists.index, top_artists.values, color='lightblue', edgecolor='black')
        plt.title("Top 10 Nghệ sĩ (Matplotlib)")
        plt.xlabel("Artist")
        plt.ylabel("Số lượng bài hát")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


class PopularityHistogram_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        plt.hist(self.data["Popularity"], bins=20, color='orange', edgecolor='black')
        plt.title("Phân bố độ phổ biến (Matplotlib)")
        plt.xlabel("Popularity")
        plt.ylabel("Số lượng bài hát")
        plt.tight_layout()
        plt.show()


class ScatterPkstreams_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        sample = self.data.sample(n=500, random_state=42) if len(self.data) > 500 else self.data
        plt.scatter(sample["Pkstreams"], sample["Popularity"], alpha=0.6, c='red')
        plt.title("Pkstreams vs Popularity (Matplotlib)")
        plt.xlabel("Pkstreams")
        plt.ylabel("Popularity")
        plt.tight_layout()
        plt.show()


class LineWks_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        wks_avg = self.data.groupby("Wks")["Popularity"].mean()
        plt.plot(wks_avg.index, wks_avg.values, marker='o', color='green')
        plt.title("Xu hướng Popularity theo Wks (Matplotlib)")
        plt.xlabel("Wks")
        plt.ylabel("Popularity trung bình")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class Heatmap_MPL(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 8))
        corr = self.data.select_dtypes(include='number').corr()
        plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
        plt.colorbar(label="Hệ số tương quan")
        plt.xticks(range(len(corr)), corr.columns, rotation=45, ha='right')
        plt.yticks(range(len(corr)), corr.columns)
        plt.title("Ma trận tương quan (Matplotlib)")
        plt.tight_layout()
        plt.show()


# ---------------------- SEABORN ----------------------

class ArtistBarChart_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 5))
        top_artists = self.data["Artist"].value_counts().head(10).index
        sns.barplot(data=self.data[self.data["Artist"].isin(top_artists)],
                    x="Artist", y="Popularity", errorbar=None, palette="Blues_r")
        plt.title("Top 10 Nghệ sĩ có độ phổ biến cao nhất (Seaborn)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


class PopularityHistogram_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        sns.histplot(self.data["Popularity"], bins=20, kde=True, color="skyblue")
        plt.title("Phân bố độ phổ biến bài hát (Seaborn)")
        plt.xlabel("Popularity")
        plt.ylabel("Số lượng bài hát")
        plt.tight_layout()
        plt.show()


class GenreBoxPlot_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 6))
        top_genres = self.data["Genre"].value_counts().head(5).index
        sns.boxplot(data=self.data[self.data["Genre"].isin(top_genres)],
                    x="Genre", y="Popularity", palette="Set3")
        plt.title("So sánh độ phổ biến theo thể loại (Seaborn)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


class ScatterPkstreams_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(8, 5))
        sample = self.data.sample(n=500, random_state=42) if len(self.data) > 500 else self.data
        sns.scatterplot(data=sample, x="Pkstreams", y="Popularity", hue="Genre", alpha=0.7)
        plt.title("Mối quan hệ giữa Pkstreams và Popularity (Seaborn)")
        plt.tight_layout()
        plt.show()


class Heatmap_SNS(BasePlot):
    def draw(self):
        plt.figure(figsize=(10, 8))
        corr = self.data.select_dtypes("number").corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Ma trận tương quan giữa các thuộc tính số (Seaborn)")
        plt.tight_layout()
        plt.show()


# ---------------------- MAIN ----------------------

def main():
    path = "data lab.csv"

    plots = [
        ArtistBarChart_MPL(path),
        PopularityHistogram_MPL(path),
        ScatterPkstreams_MPL(path),
        LineWks_MPL(path),
        Heatmap_MPL(path),
        ArtistBarChart_SNS(path),
        PopularityHistogram_SNS(path),
        GenreBoxPlot_SNS(path),
        ScatterPkstreams_SNS(path),
        Heatmap_SNS(path)
    ]

    # Test chạy từng biểu đồ (gọi một hoặc vài cái tuỳ bạn)
    #plots[0].draw()
    #plots[1].draw()
    #plots[2].draw()
    #plots[3].draw()
    #plots[4].draw()
    #plots[5].draw()
    #plots[6].draw()
    #plots[7].draw()
    #plots[8].draw()
    #plots[9].draw()


if __name__ == "__main__":
    main()
