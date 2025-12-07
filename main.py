import os
import sys
import tempfile
import urllib.request
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
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
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.validation import joblib

matplotlib.use("Qt5Agg")

APP_DIR = Path.home() / ".mall_analyzer"
APP_DIR.mkdir(exist_ok=True)
MODEL_FILE = APP_DIR / "mall_model.pkl"

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
        self.setWindowTitle("Mall Gaming Booth Analyzer + AI")
        self.setGeometry(200, 200, 700, 520)
        self.df = None
        self.model = None

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.info_label = QLabel("📊 Upload your mall visitor dataset (.csv)")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.info_label)

        self.load_button = QPushButton("Load CSV File")
        self.sample_button = QPushButton("Download Sample data")
        self.predict_button = QPushButton("AI Predict Best Setup")
        self.predict_button.setEnabled(False)

        self.load_button.clicked.connect(self.load_csv)
        self.sample_button.clicked.connect(self.download_csv)
        self.predict_button.clicked.connect(self.run_ai)

        button_row = QHBoxLayout()
        button_row.addWidget(self.load_button)
        button_row.addWidget(self.sample_button)
        button_row.addSpacing(10)

        self.main_layout.addLayout(button_row)
        self.main_layout.addWidget(self.predict_button)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.main_layout.addWidget(self.result_box)

        self.show_plot_button = QPushButton("Show Visualizations")
        self.show_plot_button.clicked.connect(self.show_plots)
        self.show_plot_button.setEnabled(False)
        self.main_layout.addWidget(self.show_plot_button)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV file", "", "CSV files (*.csv)"
        )
        if file_path:
            self.process_csv(file_path)

    def download_csv(self):
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "sample.csv")
        try:
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/kvmvkxnt/csit040_final_project/refs/heads/main/mall_kiosk.csv",
                file_path,
            )
            self.process_csv(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download CSV file:\n{e}")

    def process_csv(self, file_path):
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

        df = df[REQUIRED_COLUMNS]
        df.columns = ["Mall", "Age_Group", "Day", "Time", "Total_Bill"]

        self.df = df
        self.train_ml_model()
        self.analyze_data()

    def train_ml_model(self):
        if self.df is None:
            return
        df: pd.DataFrame = pd.DataFrame(self.df.copy())

        # Columns we'll use as features (order matters)
        feature_cols = ["Mall", "Age_Group", "Day", "Time"]

        # Build mapping encoders (LabelEncoder-like but with dict -> int)
        encoders: dict[str, dict[str, int]] = {}
        for col in feature_cols:
            series: pd.Series = df.loc[:, col].astype(str)
            uniques = pd.unique(series)

            mapping = {val: idx for idx, val in enumerate(uniques)}
            encoders[col] = mapping

            # replace values with ints in df (use mapping)
            df.loc[:, col] = series.map(lambda x: mapping[x]).astype(int)

        # Features and target
        X = df[feature_cols].copy()
        y = (df["Total_Bill"] > df["Total_Bill"].median()).astype(int)

        # Train model
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X, y)

        # Save model + encoders + feature names
        payload = {
            "model": model,
            "encoders": encoders,  # dict of dicts {col: {cat: int}}
            "feature_names": feature_cols,  # ordered list
        }
        joblib.dump(payload, MODEL_FILE)
        self.model = model
        self.encoders = encoders
        self.feature_names = feature_cols
        self.predict_button.setEnabled(True)

    def run_ai(self):
        if not os.path.exists(MODEL_FILE):
            QMessageBox.warning(self, "AI Not Ready", "Train or load data first")
            return

        ml_data = joblib.load(MODEL_FILE)
        model = ml_data["model"]
        enc = ml_data["encoders"]
        feature_names = ml_data["feature_names"]  # ordered list

        if self.df is None:
            return
        df = self.df.copy()

        # Build aggregated test rows (one row per unique combination)
        test = (
            df.groupby(["Mall", "Day", "Time", "Age_Group"], dropna=False)["Total_Bill"]
            .mean()
            .reset_index()
        )

        # Transform using saved mapping; unknown -> -1
        for col in feature_names:
            mapper = enc[col]  # dict mapping str->int from training
            # ensure string keys (we stored str earlier)
            test[col] = test[col].astype(str).map(lambda v: mapper.get(v, -1))

        # Now create final feature matrix with exact ordering and drop extras
        X_test = test[feature_names].copy()
        # Ensure dtype numeric
        X_test = X_test.astype(np.int64)

        # Predict probabilities (model expects same columns and order)
        try:
            probs = model.predict_proba(X_test)[:, 1]
        except Exception as e:
            QMessageBox.critical(self, "AI Error", f"Prediction failed:\n{e}")
            return

        test["Score"] = probs

        best = test.sort_values("Score", ascending=False).iloc[0]

        # Inverse-transform best values for display: find key by value in mapping
        def inv_lookup(mapping, value):
            for k, v in mapping.items():
                if v == value:
                    return k
            return str(value)

        result = f"""
🤖 AI Recommendation Engine Result

🏬 Best Mall → {inv_lookup(enc["Mall"], int(best["Mall"]))}
📅 Best Day → {inv_lookup(enc["Day"], int(best["Day"]))}
🕒 Best Time → {inv_lookup(enc["Time"], int(best["Time"]))}
👥 Best Age Group → {inv_lookup(enc["Age_Group"], int(best["Age_Group"]))}

🔥 Predicted Engagement Score: {round(best["Score"] * 100, 2)}%
"""
        self.result_box.append(result)
        self.result_box.moveCursor(QTextCursor.End)

    def analyze_data(self):
        if self.df is None:
            return
        df: pd.DataFrame = pd.DataFrame(self.df)
        self.show_plot_button.setEnabled(True)

        mall_spending: pd.Series = (
            df.loc[:, ["Mall", "Total_Bill"]]
            .groupby("Mall")["Total_Bill"]
            .mean()
            .sort_values(ascending=False)
        )

        day_spending: pd.Series = (
            df.loc[:, ["Day", "Total_Bill"]]
            .groupby("Day")["Total_Bill"]
            .mean()
            .sort_values(ascending=False)
        )

        time_spending: pd.Series = (
            df.loc[:, ["Time", "Total_Bill"]]
            .groupby("Time")["Total_Bill"]
            .mean()
            .sort_values(ascending=False)
        )

        best_mall = mall_spending.idxmax()
        best_day = day_spending.idxmax()
        best_time = time_spending.idxmax()

        result_text = (
            "✅ Mall Gaming Booth Analysis Results Based on Raw Data ✅\n\n"
            f"🏬 Best Mall: {best_mall}\n"
            f"📅 Best Day: {best_day}\n"
            f"🕒 Best Time: {best_time}\n\n"
            f"💰 Average Spending by Mall:\n{mall_spending.to_string()}\n\n"
            f"💵 Average Spending by Day:\n{day_spending.to_string()}\n\n"
            f"🕓 Average Spending by Time of Day:\n{time_spending.to_string()}"
        )

        self.result_box.setText(result_text)

    def show_plots(self):
        if self.df is None:
            QMessageBox.warning(self, "No data", "Please load a CSV file first.")
            return

        df = self.df

        # 1. Average Spending By Mall
        plt.figure(figsize=(8, 5))
        mall_means = df.groupby("Mall")["Total_Bill"].mean()
        cmap = plt.colormaps.get_cmap("coolwarm")
        colors = cmap(np.linspace(0, 1, len(mall_means)))
        mall_heights = np.asarray(mall_means.values, dtype=float)

        plt.bar(mall_means.index, mall_heights, color=colors)
        plt.title("Average Spending by Mall")
        plt.xlabel("Mall")
        plt.ylabel("Average Total Bill")
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.show()

        # 2. Average Spending By Day
        plt.figure(figsize=(8, 5))
        day_means = df.groupby("Day")["Total_Bill"].mean()
        cmap = plt.colormaps.get_cmap("viridis")
        colors = cmap(np.linspace(0, 1, len(day_means)))
        day_heights = np.asarray(day_means.values, dtype=float)
        plt.bar(day_means.index, day_heights, color=colors)
        plt.title("Average Spending by Day of the Week")
        plt.xlabel("Day")
        plt.ylabel("Average Total Bill")
        plt.tight_layout()
        plt.show()

        # 3. Average Spending By Time of the Day
        plt.figure(figsize=(6, 5))
        time_means = df.groupby("Time")["Total_Bill"].mean()
        cmap = plt.colormaps.get_cmap("plasma")
        colors = cmap(np.linspace(0, 1, len(time_means)))
        time_heights = np.asarray(time_means.values, dtype=float)
        plt.bar(time_means.index, time_heights, color=colors)
        plt.title("Average Spending by Time of Day")
        plt.xlabel("Time")
        plt.ylabel("Average Total Bill")
        plt.tight_layout()
        plt.show()

        # 4. Average Spending By Time + Day
        plt.figure(figsize=(8, 5))
        grouped = df.groupby(["Time", "Day"])["Total_Bill"].mean().unstack()
        times = grouped.index
        days = grouped.columns

        x = np.arange(len(times))
        width = 0.8 / len(days)

        cmap = plt.colormaps.get_cmap("cividis")
        colors = cmap(np.linspace(0, 1, len(days)))

        for i, day in enumerate(days):
            plt.bar(x + i * width, grouped[day], width, label=day, color=colors[i])
        xtick_labels = [str(t) for t in times]
        plt.xticks(x + width * (len(days) - 1) / 2, xtick_labels)
        plt.title("Average Spending by Time of Day and Day")
        plt.xlabel("Time")
        plt.ylabel("Average Total Bill")
        plt.legend(title="Day")
        plt.tight_layout()
        plt.show()

        # 5. Heatmap Age Group * Time
        pivot = df.groupby(["Age_Group", "Time"])["Total_Bill"].mean().unstack()

        plt.figure(figsize=(7, 5))
        plt.imshow(pivot, cmap=plt.colormaps.get_cmap("viridis"), aspect="auto")
        plt.colorbar(label="Average Total Bill")

        xtick_labels = [str(c) for c in pivot.columns]
        ytick_labels = [str(r) for r in pivot.index]

        plt.xticks(np.arange(len(pivot.columns)), xtick_labels)
        plt.yticks(np.arange(len(pivot.index)), ytick_labels)
        plt.title("Average Spending by Age Group and Time of Day")

        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                value = pivot.iloc[i, j]
                plt.text(
                    j,
                    i,
                    f"{value:.1f}",
                    ha="center",
                    va="center",
                    color="white"
                    if value > pivot.to_numpy(dtype=float).mean()
                    else "black",
                )
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MallAnalyzer()
    window.show()
    sys.exit(app.exec_())
