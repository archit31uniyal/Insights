import psycopg2
import requests
import os
from datasets import load_dataset


conn_str = {
        'user': os.environ['USERNAME'].lower(),
        'host': 'localhost',
        'port': 5432,
        'database': 'insights'
    }

# Connect to PostgreSQL database
# conn = psycopg2.connect(
#     dbname="insights",
#     user="postgres",
#     password=None,
#     host="localhost"
# )
conn = psycopg2.connect(**conn_str)
cur = conn.cursor()

reviews = load_dataset("McAuley-Lab/Amazon-Reviews-2023")
print(len(reviews))

# Insert data into PostgreSQL
for review in reviews:
    cur.execute("INSERT INTO reviews (text, rating) VALUES (%s, %s)", (review['text'], review['rating']))

conn.commit()
cur.close()
conn.close()
