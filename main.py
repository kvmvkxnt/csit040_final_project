import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv("./mall_kiosk.csv")

df = df[["Location", "age group", "Day of the week", "Time of the day", "Total bill"]]

df.columns = ["Mall", "Age_Group", "Day", "Time", "Total_Bill"]

print("Missing values per column:\n", df.isnull().sum(), "\n")

print("Dataset shape:", df.shape)
print("Data preview:", df.head())
print("Summary statistics:\n", df["Total_Bill"].describe())

mall_spending = df.groupby("Mall")["Total_Bill"].mean().sort_values(ascending=False)
print("\nAverage Spending by Mall:\n", mall_spending)

day_spending = df.groupby("Day")["Total_Bill"].mean().sort_values(ascending=False)
print("\nAverage Spending by Day:\n", day_spending)

time_spending = df.groupby("Time")["Total_Bill"].mean().sort_values(ascending=False)
print("\nAverage Spending by Time:\n", time_spending)

age_spending = df.groupby(["Age_Group", "Time"])["Total_Bill"].mean().unstack()
print("\nAverage Spending by Age Group and Time:\n", age_spending)

plt.figure(figsize=(8, 5))
sns.barplot(x=mall_spending.index, y=mall_spending.values, palette="coolwarm")
plt.title("Average Spending by Mall")
plt.ylabel("Average Total Bill")
plt.xlabel("Mall")
plt.xticks(rotation=15)
plt.show()

plt.figure(figsize=(8, 5))
sns.barplot(x=day_spending.index, y=day_spending.values, palette="viridis")
plt.title("Average Spending by Day of the Week")
plt.ylabel("Average Total Bill")
plt.xlabel("Day")
plt.show()

plt.figure(figsize=(6, 5))
sns.barplot(x=time_spending.index, y=time_spending.values, palette="plasma")
plt.title("Average Spending by Time of Day")
plt.ylabel("Average Total Bill")
plt.xlabel("Time of Day")
plt.show()

plt.figure(figsize=(8, 5))
sns.heatmap(age_spending, annot=True, cmap="mako", fmt=".1f")
plt.title("Spending by Age Group and Time of Day")
plt.show()

best_mall = mall_spending.idxmax()
best_day = day_spending.idxmax()
best_time = time_spending.idxmax()

print("\n🎯 Recommendations:")
print(f"- Best Mall to open the booth: {best_mall}")
print(f"- Best Day for highest engagement: {best_day}")
print(f"- Best Time of Day: {best_time}")
