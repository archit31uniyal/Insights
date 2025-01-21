from flask import Flask, render_template, request
from llama_cpp import Llama
import numpy as np
from utils import *
from transformers import AutoModelForSequenceClassification, pipeline
import os
import json
from flask_cors import CORS
import time

start_time = time.time()

app = Flask(__name__)
CORS(app, origins="*")
history = []

@app.route("/url", methods=['POST'])
def fetch_reviews():
    payload = request.get_json()
    url = payload.get("url")
    reviews = Review(url)
    reviews.fetch_reviews()
    return {
        "name": reviews.restaurant_name,
        "rating": reviews.rating,
        "text": reviews.text
    }

# @app.route("/", methods=['GET', 'POST'])
# def home():
#     answer = ""
#     submitted_text = None
#     url = None

#     if request.method == 'POST':
#         if not url:
#             url = request.form['url']
#         reviews = Review(url)
#         reviews.fetch_reviews()

#         submitted_text = request.form['textbox']
#         answer = get_response(reviews, submitted_text)
#         history.append((submitted_text, answer))

#     return render_template("home.html", message=history)

# @app.route("/app", methods=['GET', 'POST'])
# def app_response():
#     answer = ""
#     submitted_text = request.args.get('text')
    
#     if request.method == 'POST' or request.method == 'GET':
#         answer = get_response(submitted_text)
#         history.append((submitted_text, answer))

#     # return render_template("home.html", message=history)
#     return answer

def summarize_in_batches(text, llm, q_len, batch_size= 20):
    curr_pos = 0
    prev_pos = 0
    summary = []
    for i in range(batch_size):
        count = 0
        for j, t in enumerate(text[prev_pos:]):
            count += len(t.split())
            if count <= 500:
                curr_pos = j
            else:
                curr_pos += 1 
                break
        revs = ' '.join(text[prev_pos: curr_pos])
        response = llm.create_chat_completion(
            messages = [
                {"role": "system", "content": "You are an assistant who perfectly answers questions based on the reviews provided."},
                {
                    "role": "user",
                    "content": f"Context:\n {revs}\n\n Summarize the reviews preserving important information."
                }
            ]
        )
        prev_pos = curr_pos
        summary.append(response["choices"][0]["message"]["content"])
    
    response = llm.create_chat_completion(
            messages = [
                {"role": "system", "content": "You are an assistant who perfectly answers questions based on the reviews provided."},
                {
                    "role": "user",
                    "content": f"Here's a list of reviews:\n {summary}\n\n Summarize the reviews preserving important information in {4096 - q_len} words."
                }
            ]
        )
    
    return response["choices"][0]["message"]["content"]

@app.route("/response", methods=["POST"])
def get_response():
    payload = request.get_json()
    reviews = payload.get("reviews")
    question = payload.get("question")
    name = reviews["name"]
    print(name)
    q_len = len(question.split())
    sentiment_map = {
    "positive": 1,
    "negative": 0
    }

    # sentiment_llm = AutoModelForSequenceClassification.from_pretrained("gilf/english-yelp-sentiment")
    sentiment_llm = pipeline("text-classification")

    sentiment = sentiment_llm(question)
    question_class = sentiment[0]["label"]
    question_class = question_class.strip().lower()

    llm = Llama.from_pretrained(
        repo_id="unsloth/Llama-3.2-3B-Instruct-GGUF",
	    filename="Llama-3.2-3B-Instruct-Q4_K_M.gguf",
        n_ctx = 4096,
        n_gpu_layers=30
    )

    ratings = np.array(reviews.get("rating"))
    if sentiment_map[question_class]: 
        indices = np.where(ratings > 3.0)[0]
    else:
        indices = np.where(ratings < 3.0)[0]

    # Insert your environment key 
    text = reviews.get("text")

    text = [t for i, t in enumerate(text) if i in indices]
    end_time = time.time()
    time_passed = abs(end_time - start_time)
    # if os.path.exists(f"summary_reviews_{question_class}.pkl"):
    if time_passed < 86400 and os.path.exists(f"summary_{name}_reviews_{question_class}.pkl"):
        summary = load_pickle(f"summary_{name}_reviews_{question_class}.pkl")
    else:
        summary = summarize_in_batches(text, llm, q_len)
        save_pickle(summary, f"summary_{name}_reviews_{question_class}.pkl")

    response = llm.create_chat_completion(
        messages = [
            {"role": "system", "content": "You are an assistant who perfectly answers questions based on the reviews provided."},
            {
                "role": "user",
                "content": f"Here's a summary of reviews:\n {summary} \n\n Based on the summary above, answer the following question with correct grammer, \n{question}"
            }
        ]
    )

    processed = response["choices"][0]["message"]["content"]
    return processed

@app.route("/new_chat", methods=["POST"])
def new_chat():
    data = request.get_json()
    



if __name__ == "__main__":
    app.run(debug=True, port=5000)