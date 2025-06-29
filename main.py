import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("studentsperformance (2).db")
cur = conn.cursor()

cur.execute("SELECT gender, `writing score`, `reading score` FROM StudentsPerformance WHERE `writing score` > 90")
rows = cur.fetchall()
print("წერის ქულა 90-ზე მეტი:")
for i in rows:
    print(i)

# insert new
g = input("gender: ")
r = input("race: ")
p = input("parent education: ")
l = input("lunch: ")
prep = input("prep course: ")
m = int(input("math score: "))
read = int(input("reading score: "))
w = int(input("writing score: "))

cur.execute("""
INSERT INTO StudentsPerformance (
    gender, `race/ethnicity`, `parental level of education`, lunch,
    `test preparation course`, `math score`, `reading score`, `writing score`
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (g, r, p, l, prep, m, read, w))
conn.commit()

# update
gen = input("update math score for gender: ")
new_math = int(input("new math score: "))
cur.execute("UPDATE StudentsPerformance SET `math score` = ? WHERE gender = ?", (new_math, gen))
conn.commit()

# delete
limit = int(input("delete students with reading score under: "))
cur.execute("DELETE FROM StudentsPerformance WHERE `reading score` < ?", (limit,))
conn.commit()

# plots
df = pd.read_sql_query("SELECT * FROM StudentsPerformance", conn)

plt.hist(df['reading score'], bins=15, color='skyblue', edgecolor='black')
plt.title("Reading score histogram")
plt.xlabel("Score")
plt.ylabel("Count")
plt.show()

mean_scores = df.groupby("gender")[["math score", "reading score", "writing score"]].mean()
mean_scores.plot(kind="bar")
plt.title("Avg scores by gender")
plt.ylabel("Score")
plt.xticks(rotation=0)
plt.show()

prep_counts = df['test preparation course'].value_counts()
plt.pie(prep_counts, labels=prep_counts.index, autopct="%1.1f%%")
plt.title("Test prep course %")
plt.show()

conn.close()


