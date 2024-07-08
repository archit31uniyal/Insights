import psycopg2
import requests
from datasets import load_dataset

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="insights",
    user="archit",
    password="BuildRag",
    host="localhost"
)
cur = conn.cursor()

reviews = load_dataset("McAuley-Lab/Amazon-Reviews-2023")
print(len(reviews))

exit()

# Insert data into PostgreSQL
for review in reviews:
    cur.execute("INSERT INTO reviews (text, rating) VALUES (%s, %s)", (review['text'], review['rating']))

conn.commit()
cur.close()
conn.close()
