import sys
import pandas as pd
import os
import tempfile
from pandas.core import window
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import urllib.request
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt

matplotlib.use("Qt5Agg")

REQUIRED_COLUMNS = [
    "Location",
    "age group",
    "Day of the week",
    "Time of the day",
    "Total bill",
]


class MallAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mall Gaming Booth Analyzer")
        self.setGeometry(200, 200, 700, 500)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.info_label = QLabel("📊 Upload your mall visitor dataset (.csv)")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info_label)

        self.load_button = QPushButton("Load CSV File")
        self.download_sample_button = QPushButton("Download and use data")
        self.load_button.clicked.connect(self.load_csv)
        self.download_sample_button.clicked.connect(self.download_csv)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.load_button)
        self.button_layout.addWidget(self.download_sample_button)
        self.button_layout.addSpacing(10)

        self.layout.addLayout(self.button_layout)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.layout.addWidget(self.result_box)

        self.show_plot_button = QPushButton("Show Visualizations")
        self.show_plot_button.clicked.connect(self.show_plots)
        self.show_plot_button.setEnabled(False)
        self.layout.addWidget(self.show_plot_button)

        self.df: pd.DataFrame | pd.Series | None = None

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV file", "", "CSV files (*.csv)"
        )
        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV file:\n{e}")
            return

        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            QMessageBox.warning(
                self,
                "Invalid File",
                f"The following required collumns are missing:\n{', '.join(missing_cols)}",
            )
            return

        df = df[
            [
                "Location",
                "age group",
                "Day of the week",
                "Time of the day",
                "Total bill",
            ]
        ]
        df.columns = ["Mall", "Age_Group", "Day", "Time", "Total_Bill"]

        self.df = df
        self.analyze_data()

    def download_csv(self):
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "sample.csv")
        try:
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/kvmvkxnt/csit040_final_project/refs/heads/main/mall_kiosk.csv",
                file_path,
            )
            df = pd.read_csv(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV file:\n{e}")
            return

        df = df[
            [
                "Location",
                "age group",
                "Day of the week",
                "Time of the day",
                "Total bill",
            ]
        ]
        df.columns = ["Mall", "Age_Group", "Day", "Time", "Total_Bill"]

        self.df = df
        self.analyze_data()

    def analyze_data(self):
        df = self.df

        mall_spending = (
            df.groupby("Mall")["Total_Bill"].mean().sort_values(ascending=False)
        )
        day_spending = (
            df.groupby("Day")["Total_Bill"].mean().sort_values(ascending=False)
        )
        time_spending = (
            df.groupby("Time")["Total_Bill"].mean().sort_values(ascending=False)
        )

        best_mall = mall_spending.idxmax()
        best_day = day_spending.idxmax()
        best_time = time_spending.idxmax()

        result_text = (
            "✅ Mall Gaming Booth Analysis Results ✅\n\n"
            f"🏬 Best Mall: {best_mall}\n"
            f"📅 Best Day: {best_day}\n"
            f"🕒 Best Time: {best_time}\n\n"
            f"💰 Average Spending by Mall:\n{mall_spending.to_string()}\n\n"
            f"💵 Average Spending by Day:\n{day_spending.to_string()}\n\n"
            f"🕓 Average Spending by Time of Day:\n{time_spending.to_string()}"
        )

        self.result_box.setText(result_text)
        self.show_plot_button.setEnabled(True)

    def show_plots(self):
        if self.df is None:
            QMessageBox.warning(self, "No data", "Please load a CSV file first.")
            return

        df = self.df

        plt.figure(figsize=(8, 5))
        sns.barplot(x="Mall", y="Total_Bill", data=df, palette="coolwarm", ci=None)
        plt.title("Average Spending by Mall")
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(8, 5))
        sns.barplot(x="Day", y="Total_Bill", data=df, palette="viridis", ci=None)
        plt.title("Average Spending by Day of the Week")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(6, 5))
        sns.barplot(x="Time", y="Total_Bill", data=df, palette="plasma", ci=None)
        plt.title("Average Spending by Time of Day")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(8, 5))
        sns.barplot(
            x="Time", y="Total_Bill", hue="Day", data=df, palette="mako", ci=None
        )
        plt.title("Average Spending by Time of Day and Day")
        plt.tight_layout()
        plt.show()

        pivot = df.groupby(["Age_Group", "Time"])["Total_Bill"].mean().unstack()
        plt.figure(figsize=(7, 5))
        sns.heatmap(pivot, annot=True, cmap="crest", fmt=".1f")
        plt.title("Average Spending by Age Group and Time of Day")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MallAnalyzer()
    window.show()
    sys.exit(app.exec_())
